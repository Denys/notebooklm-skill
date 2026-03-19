# TEST_QueryFlow.md

## Purpose
Automated end-to-end test suite verifying the complete query workflow — from library lookup through browser automation to response extraction. Tests SVC_AskQuestion and SVC_NotebookManager together, using mocked browser sessions to avoid real Chrome launches and network calls.

## Current Implementation Status
⚪ **PLANNED** — Required for MVP completion

## MVP Context
- **Required for Feature:** NotebookLM Query Interface (test coverage)
- **Priority:** Medium — ensures the core value-delivery path remains functional
- **Blocking:** Nothing; SVC_AskQuestion works today without automated tests

## Planned Implementation Details
- **Intended Location:** `tests/test_query_flow.py`
- **Required Interfaces:** pytest test functions; mocked SVC_BrowserSession; fixture notebooks in DATA_NotebookLibrary
- **Dependencies:** SVC_AskQuestion, SVC_NotebookManager, DATA_NotebookLibrary, CONFIG_Settings, AUTH_Manager
- **Dependents:** None (leaf node)

## Core Logic & Functionality Requirements

### Test Cases to Implement
1. **test_ask_with_notebook_url** — Direct URL: question submitted and response returned
2. **test_ask_with_notebook_id** — ID lookup: library resolves ID to URL correctly
3. **test_ask_unauthenticated** — No auth: exits 1 with auth instructions
4. **test_ask_missing_notebook_id** — Unknown ID: exits 1 with not-found message
5. **test_response_includes_followup_prompt** — Response always ends with follow-up text
6. **test_query_timeout_handled** — Simulated timeout: exits 1 with timeout message
7. **test_selector_fallback** — Primary selector fails: fallback selector used successfully
8. **test_add_and_query_notebook** — Full flow: add notebook to library, activate, query it

### Test Infrastructure
- Mock SVC_BrowserSession to return pre-built mock Page objects
- Mock page response DOM with realistic NotebookLM HTML structure
- Use temp library.json fixtures for notebook management tests
- Pre-seed DATA_AuthInfo with authenticated state for query tests

## Implementation Requirements
- **Technology:** pytest, unittest.mock, pytest-asyncio (for async browser mocking)
- **Integration Points:** Patches SVC_BrowserSession.create_session to return mock; patches CONFIG_Settings paths to tmp_path
- **Data Requirements:** Sample library.json fixtures; mock HTML response matching RESPONSE_SELECTORS
- **User Experience:** `pytest tests/test_query_flow.py` runs all tests headlessly in ~60 seconds

## Interface Definition (Planned)

```python
# tests/test_query_flow.py
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

@pytest.fixture
def mock_browser_session():
    """Return mock page with pre-built NotebookLM response"""
    mock_page = AsyncMock()
    mock_page.query_selector.return_value = MagicMock(
        text_content=AsyncMock(return_value="Source-grounded answer here.")
    )
    return mock_page

@pytest.fixture
def seeded_library(tmp_path):
    """Library with one test notebook"""
    library = {
        "notebooks": [{
            "id": "test-notebook",
            "url": "https://notebooklm.google.com/notebook/test",
            "name": "Test Notebook",
            "description": "For testing",
            "topics": ["test"],
            "active": True,
            "added_at": "2026-03-19T00:00:00Z"
        }]
    }
    ...

async def test_ask_with_notebook_url(mock_browser_session):
    ...
```

## ARC Verification Criteria

### Functional Criteria
- [ ] All 8 test cases pass with `pytest tests/test_query_flow.py`
- [ ] Tests run without real Chrome or internet access
- [ ] Response text returned from mock matches expectation
- [ ] Follow-up prompt appended to every mocked response

### Input Validation Criteria
- [ ] Missing question arg: exits 1 with usage
- [ ] Unknown notebook ID: exits 1 with helpful error

### Error Handling Criteria
- [ ] Timeout simulation produces correct exit code and message
- [ ] Auth check failure produces correct exit code and instructions

### Quality Criteria
- [ ] Mock browser responses match actual NotebookLM DOM structure
- [ ] Tests isolated — each test gets fresh tmp_path fixtures
- [ ] Tests complete in under 60 seconds total

## Implementation Notes
- Use `pytest-asyncio` since Patchright API is async
- Mock at the SVC_BrowserSession level, not Patchright level (cleaner boundary)
- Record a real NotebookLM DOM response to use as fixture HTML for realistic selector testing
- Run as part of CI/CD if GitHub Actions is added in future
