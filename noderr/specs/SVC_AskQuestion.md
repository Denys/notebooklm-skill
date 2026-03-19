# SVC_AskQuestion.md

## Purpose
Core query engine. Opens a browser session to the specified NotebookLM notebook, types the user's question into the query input, waits for Gemini's streaming response to stabilize, extracts the answer text from the DOM, and returns it. This is the primary value-delivery component of the skill.

## Current Implementation Status
🟡 **WIP** — `wip-20260319-retry` — Adding SVC_RetryLogic integration

## Implementation Details
- **Location:** `scripts/ask_question.py`
- **Current interfaces:** `python scripts/run.py ask_question.py --question "..." [--notebook-id ID | --notebook-url URL] [--show-browser]`
- **Dependencies:** SVC_BrowserSession, AUTH_Manager (checks auth first), CONFIG_Settings (selectors, timeouts), DATA_NotebookLibrary (to resolve notebook-id to URL), SVC_NotebookManager, SVC_RetryLogic (wraps browser query block)
- **Dependents:** UTIL_RunWrapper (entry point), SVC_SkillInit (exported)

## Core Logic & Functionality
1. Resolves notebook URL from `--notebook-id` (looks up DATA_NotebookLibrary) or uses `--notebook-url` directly
2. Checks authentication via AUTH_Manager; aborts if not authenticated (non-retryable)
3. Creates `RetryHandler` from SVC_RetryLogic
4. Wraps steps 5–11 in `with handler.attempt():` — full browser block is retried on transient failure
5. Opens persistent Chrome context (BrowserFactory)
6. Navigates to the notebook URL
7. Waits for page load (PAGE_LOAD_TIMEOUT = 30s)
8. Locates query input via QUERY_INPUT_SELECTORS (tries each selector in order)
9. Types question with human-like timing (StealthUtils typing speed simulation)
10. Submits query (Enter key)
11. Polls for response via RESPONSE_SELECTORS; detects streaming completion (stable for N consecutive checks)
12. On retry: `finally` block closes playwright context cleanly before next attempt
13. Extracts and returns full response text
14. Appends follow-up prompt: "EXTREMELY IMPORTANT: Is that ALL you need to know?"

## Current Quality Assessment
- **Completeness:** Fully functional for standard queries; handles English and German NotebookLM UI
- **Code Quality:** Solid async implementation with selector fallbacks
- **Test Coverage:** No automated tests; extensively tested manually
- **Documentation:** SKILL.md covers all CLI options; references/usage_patterns.md covers best practices

## Technical Debt & Improvement Areas
- Streaming detection uses polling delay — fragile if NotebookLM changes animation timing
- `--show-browser` flag useful for debugging but not formally documented in help text
- No output format option (always plain text; no JSON/structured output)

## Interface Definition

```python
# CLI:
python scripts/run.py ask_question.py \
  --question "What is the main topic?" \
  [--notebook-id <id>] \
  [--notebook-url "https://notebooklm.google.com/notebook/..."] \
  [--show-browser]

# Returns: Prints answer to stdout, exits 0 on success

# Internal usage pattern after retry integration:
from retry_logic import RetryHandler

handler = RetryHandler()  # uses MAX_RETRIES, RETRY_BACKOFF_BASE from config
with handler.attempt():
    # full browser launch → navigate → query → extract block
    answer = _run_browser_query(question, notebook_url, headless)
```

## ARC Verification Criteria

### Functional Criteria
- [ ] Given valid auth and notebook URL, returns non-empty answer
- [ ] Answer contains "EXTREMELY IMPORTANT: Is that ALL you need to know?" suffix
- [ ] `--notebook-id` correctly resolves to URL via library lookup
- [ ] `--show-browser` makes Chrome window visible

### Input Validation Criteria
- [ ] Missing `--question` exits 1 with usage message
- [ ] Missing notebook reference (no --id or --url, no active notebook) exits 1 with clear message
- [ ] Unauthenticated state exits 1 with auth instructions

### Error Handling Criteria
- [ ] Transient failures (timeout, selector miss, crash) retried via RetryHandler before exiting 1
- [ ] Auth failure is non-retryable — exits 1 immediately with auth instructions
- [ ] After all retries exhausted: exits 1 with diagnostic message from RetryExhaustedError
- [ ] QUERY_TIMEOUT_SECONDS (120s) respected per attempt; total time = timeout × retries
- [ ] Network errors during navigation retried via RetryHandler

### Quality Criteria
- [ ] Chrome process closed after each query (no orphans)
- [ ] Both QUERY_INPUT_SELECTORS tried before failing
- [ ] Both RESPONSE_SELECTORS tried before failing

## Future Enhancement Opportunities
- Add `--output-json` flag for structured output
- Add `--max-wait` flag to override QUERY_TIMEOUT_SECONDS per-invocation
- Cache last response to avoid re-querying identical questions
