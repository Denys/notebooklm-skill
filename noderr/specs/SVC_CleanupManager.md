# SVC_CleanupManager.md

## Purpose
Cleans up browser cache, authentication state, and optionally the notebook library. Used as a recovery tool when Chrome sessions become corrupted, cookies expire, or disk space needs clearing. Provides a safe reset path without requiring full reinstallation.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/cleanup_manager.py`
- **Current interfaces:** `python scripts/run.py cleanup_manager.py [--confirm] [--preserve-library]`
- **Dependencies:** DATA_BrowserState, DATA_AuthInfo, DATA_NotebookLibrary, CONFIG_Settings (paths)
- **Dependents:** UTIL_RunWrapper

## Core Logic & Functionality

### Default (no flags) — Preview Mode
1. Scans data/ directory and browser_profile/
2. Reports what would be deleted (sizes, file counts)
3. Does NOT delete anything — dry run only

### --confirm — Execute Cleanup
1. Deletes `data/browser_state/state.json` (session cookies)
2. Deletes `data/browser_state/browser_profile/` (Chrome profile)
3. Resets `data/auth_info.json` to unauthenticated
4. Deletes `data/library.json` (notebook catalog) UNLESS --preserve-library

### --preserve-library
- Combined with `--confirm`: performs all cleanup EXCEPT library.json
- Use after browser crash: clears corrupted Chrome state while keeping notebook catalog

## Current Quality Assessment
- **Completeness:** Covers all cleanup scenarios needed in practice
- **Code Quality:** Safe two-phase (preview then confirm) design prevents accidental data loss
- **Test Coverage:** No automated tests; verified through recovery workflows
- **Documentation:** SKILL.md troubleshooting section documents when to use each flag

## Technical Debt & Improvement Areas
- No selective cleanup (e.g., clear only cookies, not Chrome profile)
- Preview mode output could include size estimates (currently just file counts)
- No backup-before-delete option for library.json

## Interface Definition

```python
# CLI:
python scripts/run.py cleanup_manager.py                     # Preview only
python scripts/run.py cleanup_manager.py --confirm           # Full cleanup
python scripts/run.py cleanup_manager.py --confirm --preserve-library  # Keep notebooks

# Files affected:
# data/browser_state/state.json         — always removed on --confirm
# data/browser_state/browser_profile/   — always removed on --confirm
# data/auth_info.json                   — reset on --confirm
# data/library.json                     — removed unless --preserve-library
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Default (no flags) prints preview without deleting anything
- [ ] `--confirm` removes state.json, browser_profile/, resets auth_info.json
- [ ] `--confirm` without `--preserve-library` also removes library.json
- [ ] `--confirm --preserve-library` keeps library.json intact

### Input Validation Criteria
- [ ] Running without --confirm clearly states it's a preview
- [ ] Confirmation prompt or flag prevents accidental deletion

### Error Handling Criteria
- [ ] Missing data/ directory handled gracefully (nothing to clean)
- [ ] Partial cleanup on filesystem error reported clearly

### Quality Criteria
- [ ] Auth status correctly reset in auth_info.json after cleanup
- [ ] After cleanup, `auth_manager.py status` reports unauthenticated

## Future Enhancement Opportunities
- Add `--cookies-only` flag to clear just state.json without touching Chrome profile
- Add size reporting to preview mode
- Add `--backup-library` flag to save library.json to a dated backup before deletion
