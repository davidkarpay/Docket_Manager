# Case History System - Quick Reference Guide

## Key Files to Understand

### Python Backend (Case Extraction)
- **`case_data_extractor.py`** (550+ lines)
  - `CaseData` dataclass (lines 21-44): Defines all case fields
  - `LMStudioVisionClient` (lines 47-148): Handles vision AI extraction
  - `CasePageScraper` (lines 151-231): Browser automation
  - `CaseDataExtractorApp` (lines 234-421): Main orchestrator

- **`case_extractor_cli.py`** (450+ lines)
  - `InteractiveCLI` class: User interface

- **`court_configs.py`**
  - Court-specific configurations (selectors, URLs, rates)

### Frontend (Docket Manager)
- **`morning_docket_manager_file_database.html`** (1282 lines)
  - Case display UI
  - Notes management
  - File-based database operations
  - Search and filtering

## Core Data Structures

### CaseData (Python Dataclass)
```
Required: case_number, client_name
Optional: 18+ fields (dates, charges, attorney, judge, etc.)
Special: raw_extraction (for debugging), extracted_at (timestamp)
```

### Database JSON (docket_database.json)
```json
{
  "version": "1.0",
  "lastModified": "ISO timestamp",
  "cases": [{ CSV-like objects }],
  "schema": ["field1", "field2", ...]
}
```

### In-Memory Structures (JavaScript)
- `casesData[]`: Array of case objects
- `notesData{}`: caseId → note text
- `caseMetadata{}`: caseId → quick reference info

## Storage Hierarchy

1. **Application Memory** (cleared on page reload)
   - casesData, notesData, caseMetadata

2. **Browser localStorage** (persistent in current browser)
   - docketNotes
   - docketCaseMetadata

3. **File System** (persistent across devices)
   - docket_database.json (user-selected directory)
   - NOTE: Does NOT include notes!

## Field Categories

### Identity (Required)
- case_number, client_name

### Scheduling
- next_date

### Parties
- attorney, judge, victim_info

### Classification
- charges, division, status

### Timeline
- arrest_date, filing_date, disposition, sentence

### Financial
- bond_amount

### History
- plea, prior_record, probation_info

### Administrative
- notes, page_url, extracted_at, raw_extraction

## Data Flow Summary

```
Court Website
    ↓
Screenshot (Playwright)
    ↓
Vision AI (LM Studio)
    ↓
CaseData object (Python)
    ↓
CSV/JSON Export
    ↓
HTML UI (Docket Manager)
    ↓
localStorage + optional file database
```

## What's NOT in Case History

The current system does NOT track:
- When case fields changed
- Who modified the case
- Previous versions of case data
- Timestamps on notes
- Activity/event log
- Revision history

See CASE_HISTORY_ANALYSIS.md for details on adding these features.

## CSV Import Behavior

- Flexible headers (auto-maps from any CSV format)
- Deduplication by case number (append vs. replace)
- Auto-save to localStorage
- Optional auto-save to file database
- Display as case cards with notes sections

## Search Capability

- Real-time substring search
- Case-insensitive
- Searches all visible fields
- NO advanced filtering or field-specific search
- NO historical event search

## Vision AI Extraction

- Accuracy: 90-95% typical
- Speed: 5-10 seconds per case
- Model: LLaVA 7B (locally run)
- Server: LM Studio (OpenAI-compatible API)
- Extraction temperature: 0.1 (low, for factual data)

## Important Limitations

1. **Notes Persistence Issue**
   - Notes stored ONLY in localStorage
   - NOT saved to docket_database.json
   - Lost if browser cache cleared
   - Not synced between browsers

2. **No Version Control**
   - Case data overwrites on re-import
   - Cannot see case history
   - No rollback capability

3. **No Event Tracking**
   - Cannot search by when things happened
   - No audit trail
   - No activity timeline

4. **Single-User Only**
   - File System Access API (browser-based)
   - No concurrent user support

## For Case History Implementation

The branch name suggests case history search is being added. Key additions should include:

1. **Event Log**: Track case_imported, note_added, field_changed events
2. **Notes Timeline**: Timestamp each note entry
3. **Case Revisions**: Store snapshots of case data with versions
4. **Advanced Search**: By event type, date range, field changes
5. **Activity Feed**: Chronological view of all case changes

See CASE_HISTORY_DATA_STRUCTURES.md section 10 for proposed schema.

## File Size Reference

| File | Size | Purpose |
|------|------|---------|
| case_data_extractor.py | 18KB | Main extraction engine |
| case_extractor_cli.py | 16KB | Interactive interface |
| morning_docket_manager_file_database.html | 45KB | Full docket UI |
| CASE_HISTORY_ANALYSIS.md | 17KB | Detailed architecture |
| CASE_HISTORY_DATA_STRUCTURES.md | 21KB | Visual references |

## Key Takeaways

1. **Simple Architecture**: CSV → Vision AI → JSON → HTML UI
2. **Local Processing**: All AI runs locally (privacy-first)
3. **File-Based DB**: No server, user controls location
4. **Flexible Schema**: Any CSV columns supported
5. **Current Gap**: No case history/versioning/events
6. **Ready to Extend**: Well-organized, documented code

## Recommended Reading Order

1. This file (overview)
2. CASE_HISTORY_ANALYSIS.md (deep dive)
3. CASE_HISTORY_DATA_STRUCTURES.md (visual reference)
4. ARCHITECTURE.md (technical details)
5. Source code: case_data_extractor.py, morning_docket_manager_file_database.html

---

**Last Updated:** 2024-11-14
**Analysis Branch:** claude/add-case-history-search-*
**Database Version:** 1.0
