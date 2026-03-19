# SVC_BrowserSession.md

## Purpose
Manages the lifecycle of Patchright browser sessions for NotebookLM automation. Implements the hybrid authentication approach: launches Chrome with a persistent user profile directory AND injects session cookies from state.json — combining both methods to work around Playwright bug #36139.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/browser_session.py`
- **Current interfaces:** Used as a Python module by SVC_AskQuestion and AUTH_Manager
- **Dependencies:** UTIL_BrowserUtils (BrowserFactory, StealthUtils), CONFIG_Settings (BROWSER_ARGS, paths), DATA_BrowserState (state.json + browser_profile/)
- **Dependents:** SVC_AskQuestion, AUTH_Manager

## Core Logic & Functionality
1. `BrowserFactory.create_browser()` — launches Patchright with `user_data_dir` pointing to `data/browser_state/browser_profile/` (persistent fingerprint)
2. After browser context creation, loads `state.json` and injects all cookies via `context.add_cookies()`
3. Also restores localStorage entries from state.json via JavaScript injection
4. Returns ready-to-use `page` object with authenticated session
5. On context exit: updated cookies written back to state.json (session refresh)

## Current Quality Assessment
- **Completeness:** Fully functional; the hybrid approach reliably authenticates with Google
- **Code Quality:** Well-abstracted; session management separated from query/auth logic
- **Test Coverage:** No automated tests; verified through hundreds of real queries
- **Documentation:** AUTHENTICATION.md explains the full technical rationale

## Technical Debt & Improvement Areas
- Cookie injection happens on every session launch (minor overhead)
- No detection of corrupted state.json (fails silently and falls back to unauthenticated)
- Browser profile directory grows over time — requires periodic cleanup via SVC_CleanupManager

## Interface Definition

```python
# Used as context manager:
async with BrowserSession(config) as page:
    await page.goto("https://notebooklm.google.com/")
    # page is authenticated and ready

# Key class:
class BrowserSession:
    def __init__(self, config: Config)
    async def __aenter__(self) -> Page
    async def __aexit__(self, *args) -> None
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Browser launches with persistent profile (user_data_dir set correctly)
- [ ] Cookies from state.json injected before navigation
- [ ] Session successfully authenticated at notebooklm.google.com
- [ ] Context closes cleanly after use (no zombie Chrome processes)

### Input Validation Criteria
- [ ] Handles missing state.json gracefully (unauthenticated session)
- [ ] Handles corrupted state.json without crashing

### Error Handling Criteria
- [ ] Browser launch failure raises informative exception
- [ ] Page navigation timeout handled by caller (SVC_AskQuestion)

### Quality Criteria
- [ ] No orphaned Chrome processes after successful/failed queries
- [ ] BROWSER_ARGS from config.py applied (anti-detection flags)

## Future Enhancement Opportunities
- Add cookie expiry detection to trigger reauth automatically
- Pool browser instances for parallel queries (performance optimization)
- Add connection validation before returning page object
