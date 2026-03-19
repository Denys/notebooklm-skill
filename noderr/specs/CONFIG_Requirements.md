# CONFIG_Requirements.md

## Purpose
Declares the Python package dependencies for the NotebookLM skill. Intentionally minimal — only two packages: patchright for browser automation and python-dotenv for optional .env configuration support.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `requirements.txt`
- **Current interfaces:** Read by pip during SVC_SetupEnvironment initialization
- **Dependencies:** None
- **Dependents:** SVC_SetupEnvironment (installs these packages into .venv)

## Core Logic & Functionality

```
patchright==1.55.2
python-dotenv==1.0.0
```

**patchright 1.55.2** — Playwright fork with anti-detection patches applied. Used instead of standard Playwright because it patches `navigator.webdriver` and other automation fingerprints at the native level, making browser sessions harder to detect as automated by Google's systems.

**python-dotenv 1.0.0** — Loads optional `.env` file from skill directory for configuration overrides (HEADLESS, STEALTH_ENABLED, TYPING_WPM_MIN/MAX, DEFAULT_NOTEBOOK_ID). Not required for basic operation.

## Current Quality Assessment
- **Completeness:** Minimal and correct for current functionality
- **Code Quality:** Version-pinned for reproducibility
- **Test Coverage:** N/A
- **Documentation:** README.md explains why patchright instead of playwright

## Technical Debt & Improvement Areas
- Patchright 1.55.2 may fall behind Playwright releases — check for updates when NotebookLM selectors break
- No upper version bound — `patchright==1.55.2` is exact pin (good for stability, bad for security updates)

## Interface Definition

```
# requirements.txt content:
patchright==1.55.2
python-dotenv==1.0.0

# Install command (managed automatically by run.py):
pip install -r requirements.txt
```

## ARC Verification Criteria

### Functional Criteria
- [ ] `pip install -r requirements.txt` completes without error
- [ ] `patchright` importable after install
- [ ] `dotenv` importable after install
- [ ] `python -m patchright install chrome` downloads Chrome after pip install

### Input Validation Criteria
- [ ] N/A — static file

### Error Handling Criteria
- [ ] N/A — pip handles version resolution errors

### Quality Criteria
- [ ] Both packages version-pinned for reproducibility
- [ ] No unnecessary dependencies (lean requirements)

## Future Enhancement Opportunities
- Add `patchright>=1.55.2,<2.0.0` range for flexibility while maintaining compatibility
- Consider adding `pytest` as a dev dependency once TEST_AuthFlow and TEST_QueryFlow are implemented
