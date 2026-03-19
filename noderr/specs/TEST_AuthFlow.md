# TEST_AuthFlow.md

## Purpose
Automated test suite verifying the complete authentication workflow — from unauthenticated state through setup to verified session, including status checks and clear operations. Ensures AUTH_Manager and DATA_BrowserState remain functional after code changes.

## Current Implementation Status
⚪ **PLANNED** — Required for MVP completion

## MVP Context
- **Required for Feature:** Authentication Management (test coverage)
- **Priority:** Medium — ensures reliability of the auth system critical path
- **Blocking:** Nothing; AUTH_Manager works today without automated tests

## Planned Implementation Details
- **Intended Location:** `tests/test_auth_flow.py`
- **Required Interfaces:** pytest test functions; mocks for browser automation; fixtures for temp data directories
- **Dependencies:** AUTH_Manager, DATA_AuthInfo, DATA_BrowserState, CONFIG_Settings
- **Dependents:** None (leaf node)

## Core Logic & Functionality Requirements

### Test Cases to Implement
1. **test_status_unauthenticated** — Fresh install, no data/: status returns `authenticated: false`
2. **test_status_authenticated** — Pre-seeded auth_info.json with `authenticated: true`: status returns correctly
3. **test_clear_removes_auth_data** — After clear: auth_info.json shows unauthenticated, state.json deleted
4. **test_setup_creates_state_file** — Mock browser login: state.json created with cookies structure
5. **test_reauth_updates_timestamp** — After reauth: `authenticated_at` timestamp updated
6. **test_status_with_corrupted_auth_info** — Corrupted JSON: returns unauthenticated without crash

### Test Infrastructure
- Use `tmp_path` pytest fixture for isolated data directories
- Mock Patchright browser for non-interactive testing (no real Chrome launch)
- Use `monkeypatch` to override CONFIG_Settings paths to tmp_path

## Implementation Requirements
- **Technology:** pytest (add as dev dependency), unittest.mock
- **Integration Points:** Patches SKILL_DIR/DATA_DIR in CONFIG_Settings to use test fixtures
- **Data Requirements:** Test fixtures with pre-built auth_info.json and state.json samples
- **User Experience:** Tests run headlessly via `pytest tests/test_auth_flow.py`

## Interface Definition (Planned)

```python
# tests/test_auth_flow.py
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

@pytest.fixture
def temp_data_dir(tmp_path):
    """Create isolated data directory for testing"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir

def test_status_unauthenticated(temp_data_dir):
    ...

def test_clear_removes_auth_data(temp_data_dir):
    ...

def test_setup_creates_state_file(temp_data_dir, monkeypatch):
    ...
```

## ARC Verification Criteria

### Functional Criteria
- [ ] All 6 test cases pass with `pytest tests/test_auth_flow.py`
- [ ] Tests run without launching a real browser
- [ ] Tests use isolated temp directories (no pollution of real data/)
- [ ] Tests complete in under 30 seconds total

### Input Validation Criteria
- [ ] Tests cover both happy path and error conditions
- [ ] Edge cases: missing files, corrupted JSON, empty directories

### Error Handling Criteria
- [ ] Test failures produce clear diagnostic output
- [ ] No test leaves files in real data/ directory

### Quality Criteria
- [ ] Tests are deterministic (no random/time dependencies)
- [ ] Test fixtures are reusable and well-named
- [ ] Each test has a clear docstring describing what it verifies

## Implementation Notes
- Add `pytest` to a new `requirements-dev.txt` (keep main requirements.txt minimal)
- Consider `pytest-asyncio` if async auth code needs testing
- Browser mocking is critical — no test should require internet access or real Google login
