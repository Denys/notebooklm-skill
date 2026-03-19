# SVC_SetupEnvironment.md

## Purpose
Creates the isolated Python virtual environment (.venv), installs all dependencies (patchright, python-dotenv), and downloads Google Chrome for Patchright browser automation. Runs automatically on first invocation via UTIL_RunWrapper.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/setup_environment.py`
- **Current interfaces:** `python scripts/run.py setup_environment.py` (or auto-invoked by run.py)
- **Dependencies:** System Python 3.13.7, pip, internet access
- **Dependents:** UTIL_RunWrapper (triggers this on first run)

## Core Logic & Functionality
1. Determines `SKILL_DIR` from script location
2. Creates `.venv/` using `python -m venv`
3. Upgrades pip inside the venv
4. Installs packages from `requirements.txt` via venv pip
5. Runs `python -m patchright install chrome` to download Google Chrome
6. Verifies installation success

## Current Quality Assessment
- **Completeness:** Fully functional; handles first-run setup end-to-end
- **Code Quality:** Clean subprocess-based implementation
- **Test Coverage:** No automated tests; verified by successful auth/query runs
- **Documentation:** Documented in README.md and SKILL.md

## Technical Debt & Improvement Areas
- No checksum verification of downloaded Chrome binary
- No version pinning of Chrome — version depends on patchright's bundled version
- Long setup time (~1-2 minutes) with no progress feedback beyond initial print statements

## Interface Definition

```python
# Auto-invoked by run.py on first use, or manually:
python scripts/run.py setup_environment.py

# Key operations:
# 1. python -m venv .venv
# 2. .venv/Scripts/pip install -r requirements.txt
# 3. .venv/Scripts/python -m patchright install chrome
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Running setup creates `.venv/` directory with correct Python version
- [ ] `patchright` importable inside venv after setup
- [ ] Chrome executable exists at patchright's expected location after setup

### Input Validation Criteria
- [ ] Handles case where `.venv/` already exists (no-op or upgrade)
- [ ] Fails gracefully if internet unavailable during Chrome download

### Error Handling Criteria
- [ ] Non-zero exit code if pip install fails
- [ ] Informative error if Chrome download fails

### Quality Criteria
- [ ] Works on both Windows (Scripts/) and Unix (bin/) paths
- [ ] Uses real Chrome (not Chromium) for Google service compatibility

## Future Enhancement Opportunities
- Add progress bar during Chrome download
- Verify Chrome binary integrity after download
- Support `--force-reinstall` flag to rebuild venv from scratch
