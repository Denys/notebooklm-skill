# AUTH_Manager.md

## Purpose
Manages Google authentication for NotebookLM access. Implements a hybrid authentication approach combining a persistent Chrome profile with manual cookie injection — a workaround for Playwright/Patchright bug #36139 where session cookies don't persist across browser launches.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/auth_manager.py`
- **Current interfaces:** `python scripts/run.py auth_manager.py [setup|status|reauth|clear]`
- **Dependencies:** CONFIG_Settings (paths), DATA_AuthInfo, DATA_BrowserState, SVC_BrowserSession (browser launch), UTIL_BrowserUtils
- **Dependents:** SVC_AskQuestion (checks auth before querying)

## Core Logic & Functionality

### setup / reauth
1. Launches Chrome with `SHOW_BROWSER=True` (user must see browser to log in)
2. Opens `https://notebooklm.google.com/` and waits up to `LOGIN_TIMEOUT_MINUTES` (10 min)
3. User manually logs in to Google in the visible browser window
4. After successful navigation to NotebookLM, captures all cookies via Patchright's `context.cookies()`
5. Saves cookies + localStorage to `data/browser_state/state.json`
6. Writes auth status to `data/auth_info.json` with timestamp and email

### status
1. Reads `data/auth_info.json`
2. Reports authenticated state, email, and last auth timestamp

### clear
1. Deletes `data/browser_state/state.json`
2. Resets `data/auth_info.json` to unauthenticated state

## Current Quality Assessment
- **Completeness:** All four subcommands functional; covers full auth lifecycle
- **Code Quality:** Well-structured with clear separation of concerns
- **Test Coverage:** No automated tests; manually verified across multiple sessions
- **Documentation:** AUTHENTICATION.md provides deep technical explanation of the hybrid approach

## Technical Debt & Improvement Areas
- No automatic detection of session expiry — user must manually run `reauth` when cookies expire
- No email-based account validation — any Google account is accepted
- 10-minute login timeout is hardcoded in config.py (LOGIN_TIMEOUT_MINUTES)
- Browser must be visible for auth — cannot automate Google login headlessly (by design, anti-bot policy)

## Interface Definition

```python
# CLI:
python scripts/run.py auth_manager.py setup    # Initial auth (browser opens)
python scripts/run.py auth_manager.py status   # Check auth state
python scripts/run.py auth_manager.py reauth   # Re-authenticate
python scripts/run.py auth_manager.py clear    # Remove auth data

# Data written:
# data/auth_info.json: {"authenticated": bool, "email": str, "timestamp": str}
# data/browser_state/state.json: Patchright storage state (cookies + localStorage)
```

## ARC Verification Criteria

### Functional Criteria
- [ ] `status` command reports correct authenticated/unauthenticated state
- [ ] `setup` opens visible Chrome window at notebooklm.google.com
- [ ] After manual login, cookies saved to `state.json`
- [ ] `clear` removes auth data and status shows unauthenticated

### Input Validation Criteria
- [ ] Invalid subcommand shows usage and exits 1
- [ ] `setup` aborts gracefully if browser closed before login

### Error Handling Criteria
- [ ] Login timeout (10 min) handled gracefully with informative message
- [ ] Missing data directory created automatically before writing auth files

### Quality Criteria
- [ ] Auth data never logged to stdout (security)
- [ ] state.json is protected by .gitignore (verified)

## Future Enhancement Opportunities
- Detect session expiry automatically and prompt for reauth
- Support multiple Google account profiles
- Add `--timeout` flag to override LOGIN_TIMEOUT_MINUTES
