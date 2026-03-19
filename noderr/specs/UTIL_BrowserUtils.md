# UTIL_BrowserUtils.md

## Purpose
Provides browser factory and stealth utility helpers for Patchright automation. Encapsulates anti-detection measures (disabling automation flags, setting realistic user agent) and browser launch configuration to prevent Google from identifying the session as bot traffic.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/browser_utils.py`
- **Current interfaces:** Python module imported by SVC_BrowserSession
- **Dependencies:** Patchright (patchright library), CONFIG_Settings (BROWSER_ARGS, USER_AGENT)
- **Dependents:** SVC_BrowserSession

## Core Logic & Functionality

### BrowserFactory
- `create_browser(playwright, user_data_dir)` — launches Chromium/Chrome with:
  - `user_data_dir` for persistent fingerprinting
  - `BROWSER_ARGS` from config.py (anti-automation flags)
  - `USER_AGENT` override

### StealthUtils
- `apply_stealth(page)` — patches JavaScript properties that reveal automation:
  - Overrides `navigator.webdriver` to `undefined`
  - Sets realistic screen dimensions and plugins
  - Adds human-like timing to interactions

## Current Quality Assessment
- **Completeness:** Covers the core anti-detection techniques needed
- **Code Quality:** Clean, focused utility classes with single responsibilities
- **Test Coverage:** No automated tests; effectiveness verified by successful Google auth
- **Documentation:** Comments explain why each stealth technique is applied

## Technical Debt & Improvement Areas
- Stealth techniques may need updates as Google improves bot detection
- No fingerprint randomization — same fingerprint every session (intentional for profile consistency)
- USER_AGENT hardcoded to Windows Chrome string — may become outdated

## Interface Definition

```python
class BrowserFactory:
    @staticmethod
    def create_browser(playwright, user_data_dir: Path) -> Browser

class StealthUtils:
    @staticmethod
    async def apply_stealth(page: Page) -> None
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Browser launches with all BROWSER_ARGS applied
- [ ] `navigator.webdriver` returns `undefined` on launched page
- [ ] User agent matches configured USER_AGENT string

### Input Validation Criteria
- [ ] Handles missing user_data_dir (creates directory automatically)

### Error Handling Criteria
- [ ] Browser launch failure propagates exception to caller

### Quality Criteria
- [ ] Anti-detection flags align with config.py BROWSER_ARGS list
- [ ] No hardcoded paths inside utility functions

## Future Enhancement Opportunities
- Add fingerprint rotation (different screen sizes, fonts per session)
- Update USER_AGENT to current Chrome version automatically
- Add detection validation test that checks webdriver flag post-launch
