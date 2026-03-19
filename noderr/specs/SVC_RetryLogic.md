# SVC_RetryLogic.md

## Purpose
Dedicated retry and recovery service for browser automation failures. Handles transient errors such as Chrome crashes, selector timeouts, rate limit responses from NotebookLM, and network interruptions — currently managed manually via cleanup_manager.py + auth_manager.py reauth.

## Current Implementation Status
⚪ **PLANNED** — Required for MVP completion

## MVP Context
- **Required for Feature:** Reliable query execution (Browser Automation)
- **Priority:** High — affects core reliability of every query
- **Blocking:** Nothing blocked (SVC_AskQuestion works without it, just not robustly)

## Planned Implementation Details
- **Intended Location:** `scripts/retry_logic.py`
- **Required Interfaces:** `RetryHandler` class with configurable retry count and backoff; callable from SVC_AskQuestion and AUTH_Manager
- **Dependencies:** SVC_BrowserSession, SVC_CleanupManager, CONFIG_Settings
- **Dependents:** SVC_AskQuestion (wrap query in retry), AUTH_Manager (retry auth on transient failure)

## Core Logic & Functionality Requirements
1. Wrap browser automation calls in a retry decorator/context manager
2. On failure: classify error type (crash vs timeout vs rate limit vs selector miss)
3. For crashes: run light cleanup (clear profile cache), relaunch browser
4. For timeouts: retry with increased wait time (exponential backoff)
5. For rate limits: wait fixed delay (30-60s) and retry
6. For selector misses: retry with fallback selectors before giving up
7. Max retries configurable (default: 3)
8. Report retry attempts to stdout for transparency
9. After max retries: raise final error with full diagnostic context

## Implementation Requirements
- **Technology:** Pure Python, no new dependencies; use existing patchright + config
- **Integration Points:** SVC_AskQuestion wraps its main query loop with RetryHandler; SVC_BrowserSession exposes a `reset()` method for retry use
- **Data Requirements:** Access to CONFIG_Settings timeouts; ability to call SVC_CleanupManager
- **User Experience:** User sees retry attempt messages; no silent failures

## Interface Definition (Planned)

```python
class RetryHandler:
    def __init__(self, max_retries: int = 3, backoff_base: float = 2.0)

    @contextmanager
    def attempt(self, error_types: tuple = (Exception,)):
        """Wrap a block with retry logic"""
        ...

# Usage in SVC_AskQuestion:
handler = RetryHandler(max_retries=3)
with handler.attempt(error_types=(TimeoutError, SelectorNotFoundError)):
    result = await query_notebooklm(page, question)
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Retries up to max_retries on specified error types
- [ ] Exponential backoff applied between retries
- [ ] Browser session reset between retries on crash errors
- [ ] Rate limit errors trigger appropriate fixed delay before retry
- [ ] Raises final error after max_retries exhausted

### Input Validation Criteria
- [ ] max_retries=0 means no retries (immediate failure)
- [ ] Accepts configurable error type tuple for targeted retry

### Error Handling Criteria
- [ ] Does not retry on non-transient errors (e.g., authentication failure)
- [ ] Full error context preserved in final exception for debugging

### Quality Criteria
- [ ] Retry attempts logged to stdout with attempt number and error reason
- [ ] No infinite loops possible (hard limit on retries)
- [ ] Compatible with async context (works with patchright async API)

## Implementation Notes
- Start with decorator pattern, migrate to context manager if async compatibility needed
- Test with simulated failures (mock SVC_BrowserSession to raise on N-th call)
- Rate limit detection requires parsing NotebookLM response content, not just HTTP status
