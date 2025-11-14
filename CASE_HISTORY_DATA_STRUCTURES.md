# Case History Data Structures - Visual Reference

## 1. Data Model Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Case Data Flow                              │
└─────────────────────────────────────────────────────────────────────┘

    Court Website         Playwright         LM Studio API
         │                    │                    │
         │──Page URL──→ Browser Automation        │
         │                    │                    │
         │              Screenshot PNG ──Base64──→ Vision Model
         │                    │         ←──JSON── │
         │                    │         Response  │
         └────────────────────┴────────────────────┘
                              │
                         Parse JSON
                              │
                    ┌─────────▼────────────┐
                    │                      │
                    │   CaseData Object    │
                    │ (Python Dataclass)   │
                    │                      │
                    └──────────┬───────────┘
                               │
                   ┌───────────┴──────────────┐
                   │                         │
              CSV Export              JSON Export
                   │                         │
              (.csv file)             (.json file)
                   │                         │
                   └──────────┬──────────────┘
                              │
                    ┌─────────▼──────────┐
                    │ Morning Docket Mgr │
                    │  (HTML Interface)  │
                    └──────────┬─────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
              localStorage         File Database
              (docketNotes)      (docket_database.json)
              (casesMetadata)
```

## 2. CaseData Class Fields Hierarchy

```python
CaseData
├── Identity Fields (REQUIRED)
│   ├── case_number: str              # Primary key
│   └── client_name: str              # Defendant name
│
├── Scheduling Fields
│   └── next_date: str               # Next court appearance
│
├── Party Information
│   ├── attorney: str                # Defense counsel
│   ├── judge: str                   # Presiding judge
│   └── victim_info: str             # Victim details
│
├── Case Classification
│   ├── charges: str                 # Comma-separated charges
│   ├── division: str                # Court division
│   └── status: str                  # Case status
│
├── Financial Information
│   └── bond_amount: str             # Bond/bail amount
│
├── Case Timeline
│   ├── arrest_date: str             # Date of arrest
│   ├── filing_date: str             # Charge filing date
│   ├── disposition: str             # Final disposition
│   └── sentence: str                # Sentencing info
│
├── Defendant History
│   ├── plea: str                    # Plea entered
│   ├── prior_record: str            # Prior criminal record
│   └── probation_info: str          # Probation details
│
├── Administrative Fields
│   ├── notes: str                   # General notes
│   ├── page_url: str                # Source URL
│   ├── extracted_at: str (ISO)      # Extraction timestamp
│   └── raw_extraction: Dict         # Raw API response
```

## 3. Database JSON Structure

```json
docket_database.json
│
├── version: "1.0"                    ← For schema versioning
│
├── lastModified: "2024-11-14T12:00:00.000Z"  ← ISO 8601 timestamp
│
├── cases: [                          ← Array of case records
│   {
│     "Case Number": "2024CF001234",
│     "Client Name": "John Doe",
│     "Next Date": "2024-12-15",
│     "Charges": "Felony DUI, Reckless Driving",
│     "Attorney": "Jane Smith",
│     "Judge": "Judge Robert Brown",
│     "Division": "Criminal Division",
│     "Status": "Pending",
│     "Bond Amount": "$50,000",
│     "Arrest Date": "2024-11-01",
│     "Filing Date": "2024-11-05",
│     "Disposition": null,            ← Null if not set
│     "Plea": null,
│     "Sentence": null,
│     "Probation Info": null,
│     "Prior Record": "2 prior convictions",
│     "Victim Info": "Name redacted",
│     "Notes": null,                  ← User-added notes field
│     (additional fields from CSV headers...)
│   },
│   {
│     "Case Number": "2024CF001235",
│     ... (next case)
│   }
│ ]
│
└── schema: [                         ← List of all field names
    "Case Number",
    "Client Name",
    "Next Date",
    "Charges",
    "Attorney",
    "Judge",
    "Division",
    "Status",
    "Bond Amount",
    "Arrest Date",
    "Filing Date",
    "Disposition",
    "Plea",
    "Sentence",
    "Probation Info",
    "Prior Record",
    "Victim Info",
    "Notes",
    ...
  ]
```

## 4. In-Memory Data Structures (JavaScript)

```javascript
// Cases Data (from database or CSV)
const casesData = [
  {
    "Case Number": "2024CF001234",
    "Client Name": "John Doe",
    "Next Date": "2024-12-15",
    "Charges": "Felony DUI",
    "Attorney": "Jane Smith",
    ... (all CSV fields)
  },
  {
    "Case Number": "2024CF001235",
    "Client Name": "Jane Smith",
    ... (next case)
  }
];

// Notes Storage
const notesData = {
  "case-0": "Met with client on 11/13. Discussed plea options. Client prefers trial.",
  "case-1": "Preliminary hearing scheduled for 12/10.",
  // Only cases with notes have entries
};

// Case Metadata (for quick reference)
const caseMetadata = {
  "case-0": {
    clientName: "John Doe",
    caseNumber: "2024CF001234",
    nextDate: "2024-12-15"
  },
  "case-1": {
    clientName: "Jane Smith",
    caseNumber: "2024CF001235",
    nextDate: "2024-12-20"
  }
};

// Case ID to Index Mapping (implicit)
// "case-0" = casesData[0]
// "case-1" = casesData[1]
```

## 5. Storage Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    Application Memory                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  casesData   │  │  notesData   │  │  caseMetadata        │  │
│  │  (array)     │  │  (object)    │  │  (object)            │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ▲                      ▲                       ▲
         │                      │                       │
    ┌────┴──────────────────────┴───────────────────────┴────┐
    │            Persistence Layer                          │
    ├────────────────────────────────────────────────────────┤
    │                                                        │
    │  localStorage (Browser)                              │
    │  ├── docketNotes: JSON string                         │
    │  └── docketCaseMetadata: JSON string                  │
    │     (Cleared when browser cache is cleared)           │
    │                                                        │
    │  File System (User-Selected Directory)               │
    │  └── docket_database.json                             │
    │     (Persistent across sessions)                      │
    │     Contains: version, lastModified, cases, schema    │
    │     Note: Does NOT include notes!                     │
    │                                                        │
    └────────────────────────────────────────────────────────┘
```

## 6. CSV Import Flow

```
CSV File Format:
┌─────────────────────────────────────────────────┐
│ Case Number,Client Name,Next Date,Charges,...   │
│ 2024CF001234,John Doe,2024-12-15,Felony DUI     │
│ 2024CF001235,Jane Smith,2024-12-20,Drug Charge │
└─────────────────────────────────────────────────┘
                     │
            Parse CSV Headers
                     │
         ┌───────────▼──────────────┐
         │  Dynamic Field Mapping   │
         │  (Headers become fields) │
         └───────────┬──────────────┘
                     │
         Check for Duplicates (by Case Number)
                     │
    ┌────────────────┴────────────────┐
    │                                  │
 Append            Replace/New Import
    │                                  │
    └────────────────┬────────────────┘
                     │
          Update casesData Array
                     │
      Update UI (Case Cards)
                     │
    Auto-save to localStorage
                     │
   (Optional) Auto-save to Database
```

## 7. Case Card UI Structure

```html
<div class="case-card" id="case-0">
  ┌────────────────────────────────────────────────────────┐
  │ Case Header                                            │
  ├────────────────────────────────────────────────────────┤
  │ John Doe              │                    📅 2024-12-15│
  │ 2024CF001234          │      (Next Date - prominent)   │
  ├────────────────────────────────────────────────────────┤
  │ Case Details (Grid)                                    │
  ├──────────────┬──────────────┬──────────────┬───────────┤
  │ Charges      │ Attorney     │ Judge        │ Division  │
  │ Felony DUI   │ Jane Smith   │ Judge Brown  │ Criminal  │
  ├──────────────┼──────────────┼──────────────┼───────────┤
  │ Status       │ Bond Amount  │ Arrest Date  │ Filing... │
  │ Pending      │ $50,000      │ 2024-11-01   │ 2024-11..│
  ├────────────────────────────────────────────────────────┤
  │ Case Notes                                             │
  ├────────────────────────────────────────────────────────┤
  │ ┌──────────────────────────────────────────────────┐   │
  │ │ Met with client on 11/13. Discussed plea options.│   │
  │ │ Client prefers trial.                           │   │
  │ │                                                  │   │
  │ │ [Text saved to notesData automatically on input] │   │
  │ └──────────────────────────────────────────────────┘   │
  └────────────────────────────────────────────────────────┘
```

## 8. Data Type Mapping

### Court Website → CaseData Conversion

```
Visual Element          Parser Field        CaseData Field
────────────────────────────────────────────────────────
"Case No. 2024-CF-001234" → "Case Number" → case_number
"Defendant: John Doe"      → "Client Name" → client_name
"Next: 12/15/2024"         → "Next Date"  → next_date*
"Charges: Felony DUI, ..."  → "Charges"    → charges
"Attorney: Jane Smith"     → "Attorney"    → attorney
"Judge: Robert Brown"      → "Judge"       → judge
"Section: Criminal"        → "Division"    → division
"Status: Pending"          → "Status"      → status
"Bond: $50,000"            → "Bond Amount" → bond_amount
"Arrested: 11/01/2024"     → "Arrest Date" → arrest_date*
"Filed: 11/05/2024"        → "Filing Date" → filing_date*
"Disposition: N/A"         → "Disposition" → disposition
"Plea: Not Entered"        → "Plea"        → plea
(as above...)              → (varies)      → *_info fields
(page URL)                 → (implicit)    → page_url
(extraction time)          → (generated)   → extracted_at

* Dates normalized to YYYY-MM-DD format by vision model
```

## 9. Current Limitations - What's Missing

```
┌──────────────────────────────────────────────────────────┐
│ CASE HISTORY FEATURES - NOT IMPLEMENTED                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ ❌ Event Log                                             │
│    - No tracking of who changed what                    │
│    - No timestamps for individual changes              │
│    - No change audit trail                             │
│                                                          │
│ ❌ Notes History                                         │
│    - Single text field (not versioned)                  │
│    - No timestamps on notes                            │
│    - No ability to see previous note versions          │
│                                                          │
│ ❌ Case Version Control                                  │
│    - Case data overwrites (not appended)               │
│    - No way to see previous case data                  │
│    - No rollback capability                            │
│                                                          │
│ ❌ Activity Timeline                                     │
│    - No chronological view of case activity            │
│    - No filtering by date range                        │
│    - No event type filtering                           │
│                                                          │
│ ❌ Advanced Search                                       │
│    - Basic substring search only                       │
│    - No field-specific search                          │
│    - No historical event search                        │
│    - No date range queries                             │
│                                                          │
│ ❌ Notes Persistence Issues                              │
│    - Notes stored only in localStorage                 │
│    - Notes NOT saved to docket_database.json           │
│    - Lost if database is cleared                       │
│    - No sync between storage locations                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 10. Recommended Data Structure for History Tracking

```javascript
// Enhanced Database Schema (v2.0) - Proposed

{
  "version": "2.0",
  "lastModified": "2024-11-14T12:00:00.000Z",
  
  "cases": [ /* existing */ ],
  "schema": [ /* existing */ ],
  
  // NEW: Event Log
  "events": [
    {
      "id": "evt-001",
      "timestamp": "2024-11-14T09:30:00.000Z",
      "caseId": "2024CF001234",
      "eventType": "case_imported",
      "details": {
        "source": "morning_docket_2024-11-14.csv"
      }
    },
    {
      "id": "evt-002",
      "timestamp": "2024-11-14T10:15:00.000Z",
      "caseId": "2024CF001234",
      "eventType": "note_added",
      "details": {
        "noteText": "Met with client on 11/13...",
        "noteIndex": 0
      }
    },
    {
      "id": "evt-003",
      "timestamp": "2024-11-14T11:00:00.000Z",
      "caseId": "2024CF001234",
      "eventType": "field_changed",
      "details": {
        "fieldName": "Status",
        "oldValue": "Pending",
        "newValue": "In Discovery"
      }
    }
  ],
  
  // NEW: Notes History (instead of single note)
  "notesHistory": {
    "2024CF001234": [
      {
        "timestamp": "2024-11-14T10:15:00.000Z",
        "text": "Met with client on 11/13. Discussed plea options.",
        "index": 0
      },
      {
        "timestamp": "2024-11-14T10:45:00.000Z",
        "text": "Client prefers trial.",
        "index": 1
      }
    ]
  },
  
  // NEW: Case Revisions (track data changes)
  "caseRevisions": {
    "2024CF001234": [
      {
        "timestamp": "2024-11-14T09:30:00.000Z",
        "revision": 1,
        "data": { /* full case data snapshot */ }
      },
      {
        "timestamp": "2024-11-14T11:00:00.000Z",
        "revision": 2,
        "data": { /* updated case data */ }
      }
    ]
  }
}
```

---

## File Locations Reference

| Component | File Path | Type |
|-----------|-----------|------|
| Case Extraction Engine | `/home/user/Docket_Manager/case_data_extractor.py` | Python |
| Interactive CLI | `/home/user/Docket_Manager/case_extractor_cli.py` | Python |
| Court Configs | `/home/user/Docket_Manager/court_configs.py` | Python |
| Docket Manager UI | `/home/user/Docket_Manager/morning_docket_manager_file_database.html` | HTML/JS |
| Database File | `~/Documents/[user-selected]/docket_database.json` | JSON |
| Extracted Cases | `/home/user/Docket_Manager/extracted_cases/` | Directory |
| Case Screenshots | `/home/user/Docket_Manager/extracted_cases/screenshots/` | PNG Images |
| Extracted CSV | `/home/user/Docket_Manager/extracted_cases/extracted_*.csv` | CSV |
| Extracted JSON | `/home/user/Docket_Manager/extracted_cases/extracted_*.json` | JSON |

