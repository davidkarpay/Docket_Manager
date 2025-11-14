# Case Management System - Architecture & Data Structure Analysis

## Executive Summary

The project consists of two integrated components:

1. **Case Data Extractor** (Python) - Extracts case data from court websites using vision AI
2. **Morning Docket Manager** (JavaScript/HTML) - File-based database system for managing and tracking cases with notes

This document details the current data structures, models, and how case history is implemented.

---

## Part 1: Case Data Model (Python Backend)

### CaseData Class Structure

**Location:** `/home/user/Docket_Manager/case_data_extractor.py` (lines 21-44)

```python
@dataclass
class CaseData:
    """Structured case data extracted from court pages"""
    case_number: str                      # Unique case identifier
    client_name: str                      # Defendant/defendant name
    next_date: Optional[str] = None       # Next court date (YYYY-MM-DD)
    charges: Optional[str] = None         # Comma-separated charges
    attorney: Optional[str] = None        # Attorney name(s)
    judge: Optional[str] = None           # Judge name
    division: Optional[str] = None        # Court division/department
    status: Optional[str] = None          # Case status
    bond_amount: Optional[str] = None     # Bond/bail amount
    arrest_date: Optional[str] = None     # Date of arrest
    filing_date: Optional[str] = None     # Filing/charge date
    disposition: Optional[str] = None     # Final disposition
    plea: Optional[str] = None            # Plea information
    sentence: Optional[str] = None        # Sentence information
    probation_info: Optional[str] = None  # Probation details
    prior_record: Optional[str] = None    # Prior record information
    victim_info: Optional[str] = None     # Victim information
    notes: Optional[str] = None           # General notes
    page_url: Optional[str] = None        # Source URL for verification
    extracted_at: Optional[str] = None    # ISO timestamp of extraction
    raw_extraction: Optional[Dict] = None # Full unprocessed response from vision AI
```

**Key Characteristics:**
- Uses Python dataclasses for type safety
- All fields optional except case_number and client_name (required for identification)
- Designed for CSV export (raw_extraction excluded from CSV)
- Supports conversion to dictionary via `asdict()`

### Vision AI Extraction Flow

**Extraction Process:**
1. Screenshot captured via Playwright browser automation
2. Screenshot converted to Base64
3. Sent to LM Studio (local vision model) with structured prompt
4. Vision model extracts visible text/structure
5. Responses parsed as JSON
6. Data mapped to CaseData fields

**Prompt Template** (from case_data_extractor.py, lines 64-97):
The vision model is prompted to extract:
- Client name
- Next court date (standardized to YYYY-MM-DD)
- All charges (comma-separated)
- Attorney information
- Judge name
- Court division
- Case status
- Bond amount
- Critical dates (arrest, filing)
- Disposition and plea information
- Probation information
- Victim information
- Additional fields in key-value format

**Accuracy:** 90-95% for standard fields (varies by page quality and court system)

---

## Part 2: Database & Persistence Model (File-Based)

### Database File Structure

**Location:** `/home/user/Docket_Manager/morning_docket_manager_file_database.html`

**File Format:** `docket_database.json` (stored in user-selected directory)

**Database Schema:**
```json
{
  "version": "1.0",
  "lastModified": "2024-11-14T12:34:56.789Z",
  "cases": [
    {
      "Case Number": "2024CF001234",
      "Client Name": "John Doe",
      "Next Date": "2024-12-15",
      "Charges": "Felony DUI",
      "Attorney": "Jane Smith",
      "Judge": "Judge Brown",
      "Division": "Criminal Division",
      "Status": "Pending",
      "Bond Amount": "$50,000",
      "Arrest Date": "2024-11-01",
      "Filing Date": "2024-11-05",
      ... (any additional fields from CSV import)
    }
  ],
  "schema": [
    "Case Number",
    "Client Name", 
    "Next Date",
    "Charges",
    ... (list of all field names)
  ]
}
```

**Key Features:**
- Version tracking for future migrations
- lastModified timestamp (ISO 8601 format)
- Dynamic schema based on imported CSV columns
- Flexible field names (supports various court systems)
- Stored as human-readable JSON (not binary)

### In-Memory Data Structures

**Global Variables** (JavaScript):
```javascript
let casesData = [];              // Array of case objects
let notesData = {};              // Object: caseId -> note text
let caseMetadata = {};           // Object: caseId -> {clientName, caseNumber, nextDate}
let databaseFileHandle = null;   // File System Access API handle
let databaseDirectoryHandle = null;
let databaseFileName = 'docket_database.json';
```

**Case Metadata Structure:**
```javascript
caseMetadata[caseId] = {
  clientName: string,     // From CSV
  caseNumber: string,     // Extracted or from CSV
  nextDate: string        // For quick reference
}
```

**Notes Structure:**
```javascript
notesData[caseId] = string;  // Freeform text notes
```

---

## Part 3: Case History Implementation

### Current Implementation

**NOTE:** The current system does NOT have formal case history/events tracking. Instead, it uses:

1. **Notes System** - Case-specific notes stored in localStorage + database
2. **Metadata** - Basic case metadata (client name, case number, next date)
3. **Timestamps** - Database lastModified timestamp (tracks when database was last saved)
4. **CSV Import History** - Cases are imported from CSV, but no change tracking per case

### Notes Storage

**Persistence Locations:**
1. **localStorage** (browser memory)
   - Key: `docketNotes` (all notes as JSON string)
   - Key: `docketCaseMetadata` (metadata as JSON string)
   - Cleared when browser cache is cleared

2. **File-based database** (persistent)
   - Stored in user-selected docket_database.json
   - Persists across browser sessions
   - Notes not stored in JSON database (only cases data)

**Code Reference:**
```javascript
// Save to localStorage
localStorage.setItem('docketNotes', JSON.stringify(notesData));

// Load from localStorage  
const savedNotes = localStorage.getItem('docketNotes');
```

### Case Card Display

**UI Components** (HTML structure):
```html
<div class="case-card">
  <div class="case-header">
    <div>
      <div class="client-name">{Client Name}</div>
      <div class="case-number">{Case Number}</div>
    </div>
    <div class="next-date">📅 {Next Date}</div>
  </div>
  
  <div class="case-details">
    <!-- All case fields displayed as key-value pairs -->
  </div>
  
  <div class="notes-section">
    <textarea class="notes-textarea" data-case-id="{caseId}">
      {Saved Notes}
    </textarea>
  </div>
</div>
```

**Display Fields:**
- Client Name (large, prominent)
- Case Number (secondary identifier)
- Next Date (highlighted in green)
- All other case fields as detail items
- Editable notes textarea for case-specific documentation

---

## Part 4: Data Flow Architecture

### Single Case Extraction (Python)

```
User Input (case_number, url)
         ↓
Playwright Browser Opens
         ↓
Navigate to Case URL + Wait for Page Load
         ↓
Capture Full-Page Screenshot (PNG)
         ↓
Convert Screenshot to Base64
         ↓
Send to LM Studio Vision API
  - Prompt: Structured extraction instructions
  - Image: Base64-encoded screenshot
         ↓
LLaVA Vision Model Processes
  - Analyzes visual content
  - Extracts text and structure
  - Returns JSON response
         ↓
Parse JSON Response
         ↓
Create CaseData Object
  - Map extracted fields to dataclass
  - Store raw_extraction for debugging
  - Add timestamp (extracted_at)
  - Add source URL (page_url)
         ↓
Save Screenshot (for audit trail)
         ↓
Export to CSV/JSON
```

**Performance:**
- Per case: 5-10 seconds
- Batch (20 cases): 5-10 minutes
- Bottleneck: AI inference time (2-4 sec per case with 7B model)

### Multiple Cases (Batch Processing)

```
Load CSV file with case numbers + URLs
         ↓
For each case:
  - Run extraction flow (above)
  - Add 3-5 second delay (rate limiting)
  - Append to results list
         ↓
Export All Results:
  - CSV: One row per case, all fields
  - JSON: Full extraction data + raw responses
```

### Docket Manager Integration

```
CSV File Upload
    ↓
Parse CSV (flexible headers)
    ↓
Detect duplicates (by case number)
    ↓
Append or replace existing cases
    ↓
Display in UI (case cards)
    ↓
User adds notes
    ↓
Auto-save to:
  - localStorage (instant)
  - File-based database (when user clicks save)
    ↓
Export options:
  - Notes as text file
  - Full database as JSON
```

---

## Part 5: Search & Filtering

### Current Search Implementation

**Search Scope:**
- Searches across all visible case text
- Case-insensitive
- Real-time as user types

**Searchable Fields:**
All case data fields are searchable by virtue of being in the case card HTML

**Code:**
```javascript
function performSearch(query) {
    const searchTerm = query.toLowerCase().trim();
    document.querySelectorAll('.case-card').forEach(card => {
        const cardText = card.textContent.toLowerCase();
        if (cardText.includes(searchTerm) || !searchTerm) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}
```

**Note:** This is basic substring matching, not advanced indexing or field-specific search.

---

## Part 6: Export Capabilities

### CSV Export

**Format:**
- Standard RFC 4180 CSV
- Headers: All unique field names from all cases (sorted alphabetically)
- Excludes: raw_extraction (too verbose for spreadsheet)

**Usage:**
```python
app.export_to_csv("extracted_cases.csv")  # Automatic filename with timestamp
```

**Code Reference:** `case_data_extractor.py`, lines 361-395

### JSON Export

**Format:**
- Array of case objects
- Includes all fields (raw_extraction for debugging)
- Pretty-printed for readability

**Usage:**
```python
app.export_to_json("extracted_cases.json")
```

**Code Reference:** `case_data_extractor.py`, lines 397-416

### Notes Export (Docket Manager)

**Format:** Plain text with formatting
```
MORNING DOCKET NOTES EXPORT
Generated: [timestamp]
Total Cases with Notes: [count]

================================================================================

CLIENT: [name]
CASE NUMBER: [number]
NEXT DATE: [date]

NOTES:
[case notes text]

================================================================================
```

**File Naming:** `docket-notes-YYYY-MM-DD.txt`

---

## Part 7: Configuration & Customization

### Court Configuration (Python)

**Location:** `/home/user/Docket_Manager/court_configs.py`

**Configurable Parameters:**
```python
{
    'name': 'Court Name',
    'case_url_template': 'https://...',
    'wait_selector': '.case-details',      # CSS selector for page readiness
    'wait_timeout': 10000,                 # Milliseconds
    'additional_wait': 2000,               # Extra wait after selector
    'rate_limit_seconds': 3,               # Between requests
    'search_selectors': {                  # For interactive search
        'case_number_input': '#caseNumber',
        'search_button': '#searchBtn',
        'result_link': '.case-link'
    },
    'custom_fields': [],                   # Jurisdiction-specific fields
    'output_dir': 'extracted_cases/[court]'
}
```

**Example Courts Configured:**
- Palm Beach County Courts
- Broward County Courts
- Template for custom courts

### Vision Model Configuration

**LM Studio Settings:**
- Model: LLaVA 1.6 Mistral 7B (default, recommended)
- Temperature: 0.1 (low - for factual extraction)
- Max tokens: 2000
- Timeout: 120 seconds

**Alternative Models Supported:**
- llava-1.5-7b
- llava-1.5-13b
- bakllava-7b

---

## Part 8: Limitations & Missing Features

### Current Limitations

1. **No History Tracking Per Case**
   - Changes to case data are not tracked
   - No audit trail of modifications
   - No version control for cases
   - No event log

2. **Notes Are Not Timestamped**
   - No record of when notes were added/modified
   - No change history for notes
   - Single textarea for all notes (can't track individual updates)

3. **Database Notes Not Persisted**
   - Notes stored only in localStorage and optional JSON file
   - If file database is used, notes aren't included
   - Notes and case data are separate systems

4. **No Multi-User Support**
   - Single browser/machine only
   - File System Access API (browser-based)
   - No concurrent access handling

5. **Search Limitations**
   - Basic substring matching
   - No field-specific search
   - No complex queries
   - No indexed search

6. **Import Deduplication Only**
   - Duplicate detection by case number only
   - No detection of case updates
   - New imports replace entire cases if reimported

### Potential Enhancements for Case History

1. **Event Log Table:**
   - Track: case created, notes added, case updated, data changed
   - Fields: timestamp, user, event_type, field_changed, old_value, new_value

2. **Case Revision History:**
   - Store previous versions of case data
   - Allow rollback to previous state
   - Track who changed what and when

3. **Notes Timeline:**
   - Timestamp each note entry
   - Show chronological history
   - Support multi-entry notes (appending vs. replacing)

4. **Activity Feed:**
   - Unified view of all changes
   - Filtered by case
   - Filtered by date range
   - Filtered by event type

5. **Audit Trail:**
   - Legal compliance tracking
   - Immutable record of changes
   - Export audit log separately

---

## Part 9: Technology Stack

### Backend (Case Extraction)

**Language:** Python 3.10+
**Key Libraries:**
- `playwright` - Browser automation
- `httpx` - Async HTTP client for LM Studio API
- `dataclasses` - Type-safe data models
- `csv` - CSV export
- `json` - JSON handling
- `asyncio` - Asynchronous operations

### Frontend (Docket Manager)

**Technology:** Vanilla JavaScript (no frameworks)
**APIs Used:**
- File System Access API (for database file I/O)
- localStorage (for notes persistence)
- DOM manipulation (for UI updates)

**No External Dependencies:** Pure HTML/CSS/JavaScript

### Vision AI

**Local Model:** LLaVA (Large Language Vision Assistant)
**Server:** LM Studio (local OpenAI-compatible API)
**Model Size:** 7B parameters (8GB RAM required)

---

## Part 10: File Structure Summary

```
/home/user/Docket_Manager/
├── Core Application
│   ├── case_data_extractor.py          (550+ lines, main extraction engine)
│   ├── case_extractor_cli.py           (450+ lines, interactive CLI)
│   └── court_configs.py                (court-specific configuration)
│
├── Configuration & Templates
│   ├── case_extractor_requirements.txt (Python dependencies)
│   └── cases_template.csv              (batch processing example)
│
├── Documentation
│   ├── ARCHITECTURE.md                 (technical deep dive)
│   ├── CASE_EXTRACTOR_GUIDE.md         (complete setup guide)
│   ├── PROJECT_SUMMARY.md              (overview)
│   ├── DEPLOYMENT_CHECKLIST.md         (step-by-step)
│   └── START_HERE.md                   (entry point)
│
├── Docket Manager
│   └── morning_docket_manager_file_database.html  (file-based db UI)
│
└── Output (created at runtime)
    └── extracted_cases/
        ├── screenshots/
        │   └── [case]_[timestamp].png
        ├── extracted_[timestamp].csv
        └── extracted_[timestamp].json
```

---

## Summary & Recommendations

### Current State

The system successfully implements:
- ✅ Case data extraction from court websites using local vision AI
- ✅ Flexible data import via CSV
- ✅ File-based persistent database with JSON storage
- ✅ Case notes with localStorage persistence
- ✅ Search and filtering of loaded cases
- ✅ Export capabilities (CSV, JSON, notes)

**Data Structure:** Simple but effective - uses CSV-like records with optional note attachments

### For Case History Search Feature

To implement case history search (as indicated by the branch name), recommend:

1. **Event Table Model:**
   - Add `events` array to database structure
   - Each event: {timestamp, eventType, caseId, details}

2. **Notes Revision Support:**
   - Change notes storage to array of entries
   - Each entry: {timestamp, text}

3. **Search Enhancements:**
   - Index events by case_id
   - Support date range queries
   - Support event type filtering

4. **Database Migrations:**
   - Version the database schema
   - Automatic upgrade on load
   - Backward compatibility

See branch `claude/add-case-history-search-*` for specific implementation requirements.

