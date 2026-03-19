# DATA_NotebookLibrary.md

## Purpose
Local JSON flat-file database storing metadata about all NotebookLM notebooks known to the skill. Acts as the bridge between notebook URLs (long, unguessable) and friendly identifiers (name, id, topics) that Claude and the user can reference naturally.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `data/library.json` (created on first `notebook_manager.py add` call)
- **Current interfaces:** Read/written by SVC_NotebookManager; read by SVC_AskQuestion for URL resolution
- **Dependencies:** CONFIG_Settings (LIBRARY_FILE path constant)
- **Dependents:** SVC_NotebookManager, SVC_AskQuestion, SVC_CleanupManager

## Core Logic & Functionality

JSON structure:
```json
{
  "notebooks": [
    {
      "id": "my-api-docs-abc123",
      "url": "https://notebooklm.google.com/notebook/<long-id>",
      "name": "My API Documentation",
      "description": "REST API docs for the internal payment service",
      "topics": ["api", "payments", "rest"],
      "active": true,
      "added_at": "2026-03-19T04:00:00Z"
    }
  ]
}
```

- `id` — URL-safe slug used as `--notebook-id` argument
- `active` — only one notebook can be active at a time
- `topics` — comma-separated list used for `search` filtering

## Current Quality Assessment
- **Completeness:** Schema covers all fields needed for current operations
- **Code Quality:** Simple JSON, no ORM complexity — appropriate for this use case
- **Test Coverage:** No automated tests; manually verified through add/list/search/activate flows
- **Documentation:** SKILL.md and references/api_reference.md document the schema

## Technical Debt & Improvement Areas
- No JSON schema validation — malformed library.json causes runtime errors
- No backup mechanism before writes — power loss during write could corrupt file
- No notebook count limit — could grow unbounded
- `id` generation not guaranteed unique across installations (though collision is extremely unlikely)

## Interface Definition

```python
# Path accessed via CONFIG_Settings:
from config import LIBRARY_FILE  # Path object pointing to data/library.json

# Access pattern in SVC_NotebookManager:
import json
with open(LIBRARY_FILE) as f:
    library = json.load(f)
# library["notebooks"] is the list of notebook dicts
```

## ARC Verification Criteria

### Functional Criteria
- [ ] library.json created automatically on first `add` if data/ directory exists
- [ ] Added notebooks persist across skill invocations
- [ ] `activate` correctly sets one `active: true`, all others `active: false`
- [ ] SVC_AskQuestion can resolve `--notebook-id` to URL using library data

### Input Validation Criteria
- [ ] Missing library.json treated as empty library (not an error)
- [ ] Corrupted JSON reports parse error with file path

### Error Handling Criteria
- [ ] Data directory creation handled by AUTH_Manager on first auth
- [ ] Read-only filesystem gracefully reported

### Quality Criteria
- [ ] File protected by .gitignore (never committed)
- [ ] Timestamps stored in ISO 8601 format

## Future Enhancement Opportunities
- Add JSON schema validation with jsonschema library
- Implement atomic write (write to temp file, then rename)
- Add `last_queried_at` field to track usage patterns
- Export/import library for backup and migration between machines
