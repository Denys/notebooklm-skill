# SVC_NotebookManager.md

## Purpose
Manages the local notebook library — a JSON-based catalog of NotebookLM notebooks with their metadata (name, description, topics, URL, ID). Provides CRUD operations for Claude to discover, add, activate, search, and remove notebooks without navigating NotebookLM manually.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/notebook_manager.py`
- **Current interfaces:** `python scripts/run.py notebook_manager.py [add|list|search|activate|remove|stats] [options]`
- **Dependencies:** DATA_NotebookLibrary (library.json), CONFIG_Settings (LIBRARY_FILE path)
- **Dependents:** SVC_AskQuestion (resolves notebook-id → URL), UTIL_RunWrapper

## Core Logic & Functionality

### add
- Requires `--url`, `--name`, `--description`, `--topics` (all mandatory)
- Generates unique notebook ID (UUID-based slug)
- Appends entry to library.json
- Supports Smart Add workflow: query first with SVC_AskQuestion, then add with discovered metadata

### list
- Reads library.json and prints all notebooks in tabular format
- Shows ID, name, description preview, topics, active status

### search
- Filters library by `--query` matching name, description, or topics (case-insensitive)

### activate
- Sets `"active": true` on specified notebook, clears active flag from all others
- SVC_AskQuestion uses active notebook if no `--notebook-id` or `--notebook-url` given

### remove
- Removes notebook entry by `--id` from library.json

### stats
- Shows total notebooks, active notebook, topic distribution

## Current Quality Assessment
- **Completeness:** All CRUD operations present and working
- **Code Quality:** Clean argparse-based implementation with JSON persistence
- **Test Coverage:** No automated tests; verified through real notebook management workflows
- **Documentation:** SKILL.md and references/api_reference.md cover all commands

## Technical Debt & Improvement Areas
- All fields required for `add` — no interactive prompt fallback; relies on Claude to gather metadata
- No duplicate URL detection — same notebook can be added multiple times
- library.json not schema-validated on read — corrupted file causes crash
- No backup before write — file corruption on interrupted write possible

## Interface Definition

```python
# CLI:
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query KEYWORD
python scripts/run.py notebook_manager.py activate --id NOTEBOOK_ID
python scripts/run.py notebook_manager.py remove --id NOTEBOOK_ID
python scripts/run.py notebook_manager.py stats

# library.json schema:
{
  "notebooks": [
    {
      "id": "slug-string",
      "url": "https://notebooklm.google.com/notebook/...",
      "name": "Notebook Name",
      "description": "What this notebook contains",
      "topics": ["topic1", "topic2"],
      "active": false,
      "added_at": "ISO timestamp"
    }
  ]
}
```

## ARC Verification Criteria

### Functional Criteria
- [ ] `add` creates entry in library.json with all required fields
- [ ] `list` shows all notebooks with name, id, active status
- [ ] `search --query X` returns only notebooks matching X in name/description/topics
- [ ] `activate --id X` sets exactly one notebook as active
- [ ] `remove --id X` deletes notebook from library

### Input Validation Criteria
- [ ] `add` without required fields exits 1 with usage message
- [ ] `activate` with unknown ID exits 1 with informative error
- [ ] `remove` with unknown ID exits 1 with informative error

### Error Handling Criteria
- [ ] Missing library.json handled (creates empty library automatically)
- [ ] Corrupted library.json reports error rather than crashing silently

### Quality Criteria
- [ ] library.json written atomically (no partial writes)
- [ ] ID generation produces unique values across multiple adds

## Future Enhancement Opportunities
- Add duplicate URL detection with `--force` override
- Add `--update` subcommand to edit existing notebook metadata
- Validate library.json schema on load with informative error messages
- Add library backup before destructive operations
