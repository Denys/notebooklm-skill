# DATA_BrowserState.md

## Purpose
Stores the complete browser state needed to resume an authenticated Google session — cookies, localStorage entries, and a persistent Chrome user profile. This two-part storage is the foundation of the hybrid authentication approach that works around Playwright/Patchright bug #36139.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `data/browser_state/` directory (created by AUTH_Manager on first auth)
  - `data/browser_state/state.json` — Patchright storage state (cookies + localStorage)
  - `data/browser_state/browser_profile/` — Full Chrome user profile directory
- **Current interfaces:** Read/written by SVC_BrowserSession; cleared by SVC_CleanupManager
- **Dependencies:** CONFIG_Settings (BROWSER_STATE_DIR, STATE_FILE, BROWSER_PROFILE_DIR paths)
- **Dependents:** SVC_BrowserSession, AUTH_Manager, SVC_CleanupManager

## Core Logic & Functionality

### state.json (Patchright storage state)
```json
{
  "cookies": [
    {
      "name": "__Secure-3PSID",
      "value": "<session-token>",
      "domain": ".google.com",
      "path": "/",
      "secure": true,
      "httpOnly": true
    }
  ],
  "origins": [
    {
      "origin": "https://notebooklm.google.com",
      "localStorage": [...]
    }
  ]
}
```

### browser_profile/ (Chrome user profile)
- Full Chrome user data directory with consistent fingerprint
- Prevents Google from flagging the session as a new/suspicious device on each run
- Contains cached resources, preferences, extension state (Chrome internals)
- Grows over time — periodic cleanup via SVC_CleanupManager recommended

## Current Quality Assessment
- **Completeness:** Both components (state.json + browser_profile/) required for hybrid auth to work
- **Code Quality:** Managed entirely by Patchright/Chrome — no custom code in these files
- **Test Coverage:** No automated tests; validity tested implicitly by successful queries
- **Documentation:** AUTHENTICATION.md explains the full rationale for this two-part approach

## Technical Debt & Improvement Areas
- browser_profile/ grows unboundedly — no automatic size limit
- state.json contains sensitive session tokens — must remain gitignored
- No expiry detection on cookies stored in state.json
- Profile directory corruption requires full cleanup + reauth

## Interface Definition

```python
# Paths via CONFIG_Settings:
from config import STATE_FILE, BROWSER_STATE_DIR, BROWSER_PROFILE_DIR

# Used by SVC_BrowserSession:
# 1. Launch Chrome with user_data_dir=BROWSER_PROFILE_DIR
# 2. Load state.json via context.add_cookies() + localStorage injection
# 3. After session: save updated cookies back to state.json
```

## ARC Verification Criteria

### Functional Criteria
- [ ] state.json created by AUTH_Manager after successful login
- [ ] browser_profile/ directory exists and contains Chrome profile data after setup
- [ ] SVC_BrowserSession successfully loads cookies from state.json into browser context
- [ ] After successful query, updated cookies written back to state.json

### Input Validation Criteria
- [ ] Missing state.json results in unauthenticated session (handled by SVC_BrowserSession)
- [ ] Empty browser_profile/ still allows browser launch (fresh profile)

### Error Handling Criteria
- [ ] Corrupted state.json logs warning and proceeds with unauthenticated session
- [ ] SVC_CleanupManager safely removes both components

### Quality Criteria
- [ ] Both state.json and browser_profile/ protected by .gitignore (critical — contains credentials)
- [ ] data/ directory created automatically before first write

## Future Enhancement Opportunities
- Add cookie expiry detection and auto-reauth trigger
- Implement profile size monitoring and automatic cleanup above threshold
- Add state.json encryption at rest for enhanced security
