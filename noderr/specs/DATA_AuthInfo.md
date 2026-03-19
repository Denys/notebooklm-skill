# DATA_AuthInfo.md

## Purpose
Persists the current authentication status of the skill's Google session. Provides a lightweight status file that scripts can check without launching a browser — avoiding expensive Chrome startup for routine status queries.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `data/auth_info.json` (created by AUTH_Manager on first auth setup)
- **Current interfaces:** Read by AUTH_Manager status command; written by AUTH_Manager setup/clear
- **Dependencies:** CONFIG_Settings (AUTH_INFO_FILE path constant)
- **Dependents:** AUTH_Manager, SVC_AskQuestion (checks auth before querying)

## Core Logic & Functionality

JSON structure:
```json
{
  "authenticated": true,
  "email": "user@gmail.com",
  "authenticated_at": "2026-03-19T04:00:00Z",
  "last_check": "2026-03-19T04:30:00Z"
}
```

- `authenticated` — boolean; primary check used by SVC_AskQuestion
- `email` — Google account email captured during setup
- `authenticated_at` — timestamp of last successful auth setup
- `last_check` — timestamp of last status verification

Note: This file records *claimed* auth status. Actual validity depends on whether the cookies in DATA_BrowserState are still accepted by Google. The two can fall out of sync (auth_info says true, but cookies expired).

## Current Quality Assessment
- **Completeness:** Sufficient for current auth workflow
- **Code Quality:** Simple JSON, appropriate for purpose
- **Test Coverage:** No automated tests
- **Documentation:** AUTH_Manager spec covers the write workflow

## Technical Debt & Improvement Areas
- No cookie expiry verification — `authenticated: true` may be stale if cookies expired
- Email field captured at setup but not re-verified on subsequent runs
- No automatic staleness detection (e.g., flag auth as stale after X days)

## Interface Definition

```python
# Path via CONFIG_Settings:
from config import AUTH_INFO_FILE

# Read pattern:
import json
with open(AUTH_INFO_FILE) as f:
    auth = json.load(f)
is_authenticated = auth.get("authenticated", False)
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Created automatically by AUTH_Manager on successful setup
- [ ] `authenticated: true` after successful Google login
- [ ] `authenticated: false` (or missing) before any setup
- [ ] Cleared/reset by `auth_manager.py clear`

### Input Validation Criteria
- [ ] Missing auth_info.json treated as unauthenticated (not error)

### Error Handling Criteria
- [ ] Corrupted JSON treated as unauthenticated with warning

### Quality Criteria
- [ ] File protected by .gitignore (never committed)
- [ ] Email never logged to stdout during normal operations

## Future Enhancement Opportunities
- Add `expires_at` field estimated from cookie expiry times
- Add automatic staleness check (if auth older than 7 days, prompt reauth)
- Encrypt email field at rest for additional privacy
