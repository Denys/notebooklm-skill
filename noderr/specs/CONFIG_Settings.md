# CONFIG_Settings.md

## Purpose
Centralized configuration module for all constants used across the NotebookLM skill scripts. Contains CSS selectors for the NotebookLM UI, file system paths, browser launch arguments, user agent, and timeout values. The single source of truth — update here when the NotebookLM UI changes.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/config.py`
- **Current interfaces:** Python module imported by all scripts that need configuration
- **Dependencies:** `pathlib.Path` (stdlib only)
- **Dependents:** AUTH_Manager, SVC_AskQuestion, SVC_BrowserSession, SVC_NotebookManager, SVC_CleanupManager, DATA_NotebookLibrary, DATA_AuthInfo, DATA_BrowserState

## Core Logic & Functionality

### Path Constants
```python
SKILL_DIR = Path(__file__).parent.parent   # Root of skill installation
DATA_DIR = SKILL_DIR / "data"
BROWSER_STATE_DIR = DATA_DIR / "browser_state"
BROWSER_PROFILE_DIR = BROWSER_STATE_DIR / "browser_profile"
STATE_FILE = BROWSER_STATE_DIR / "state.json"
AUTH_INFO_FILE = DATA_DIR / "auth_info.json"
LIBRARY_FILE = DATA_DIR / "library.json"
```

### UI Selectors (critical — update when NotebookLM UI changes)
```python
QUERY_INPUT_SELECTORS = [
    "textarea.query-box-input",                         # Primary
    'textarea[aria-label="Feld für Anfragen"]',         # German fallback
    'textarea[aria-label="Input for queries"]',         # English fallback
]
RESPONSE_SELECTORS = [
    ".to-user-container .message-text-content",         # Primary
    "[data-message-author='bot']",
    "[data-message-author='assistant']",
]
```

### Browser Configuration
```python
BROWSER_ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--no-first-run',
    '--no-default-browser-check'
]
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```

### Timeouts
```python
LOGIN_TIMEOUT_MINUTES = 10
QUERY_TIMEOUT_SECONDS = 120
PAGE_LOAD_TIMEOUT = 30000  # ms
```

## Current Quality Assessment
- **Completeness:** Covers all configuration needed by current scripts
- **Code Quality:** Clean, flat module with no logic — pure constants
- **Test Coverage:** N/A (configuration module)
- **Documentation:** Inline comments explain purpose of each selector group

## Technical Debt & Improvement Areas
- USER_AGENT hardcoded to specific Chrome version string — may become outdated
- Selectors not version-tagged — unclear which NotebookLM UI version they target
- No environment variable overrides for timeouts (though .env support exists via python-dotenv)
- QUERY_TIMEOUT_SECONDS was increased from 30 to 120 in v1.3.0 — may need tuning

## Interface Definition

```python
# Import pattern used by all scripts:
from config import (
    SKILL_DIR, DATA_DIR, BROWSER_STATE_DIR, BROWSER_PROFILE_DIR,
    STATE_FILE, AUTH_INFO_FILE, LIBRARY_FILE,
    QUERY_INPUT_SELECTORS, RESPONSE_SELECTORS,
    BROWSER_ARGS, USER_AGENT,
    LOGIN_TIMEOUT_MINUTES, QUERY_TIMEOUT_SECONDS, PAGE_LOAD_TIMEOUT
)
```

## ARC Verification Criteria

### Functional Criteria
- [ ] All path constants resolve correctly relative to skill installation directory
- [ ] QUERY_INPUT_SELECTORS match current NotebookLM textarea element
- [ ] RESPONSE_SELECTORS match current NotebookLM response container
- [ ] BROWSER_ARGS suppress `navigator.webdriver` detection

### Input Validation Criteria
- [ ] N/A — pure constants module, no input

### Error Handling Criteria
- [ ] N/A — no runtime logic

### Quality Criteria
- [ ] No hardcoded absolute paths — all paths relative to SKILL_DIR
- [ ] Single import covers all needed constants (no partial imports required)

## Future Enhancement Opportunities
- Add .env override support for QUERY_TIMEOUT_SECONDS and LOGIN_TIMEOUT_MINUTES
- Tag selectors with NotebookLM UI version they were validated against
- Auto-update USER_AGENT from Chrome release channel
