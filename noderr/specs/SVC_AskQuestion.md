# SVC_AskQuestion.md

## Purpose
Core query engine. Opens a browser session to the specified NotebookLM notebook, types the user's question into the query input, waits for Gemini's streaming response to stabilize, extracts the answer text from the DOM, and returns it. This is the primary value-delivery component of the skill.

## Current Implementation Status
🟢 **VERIFIED** — `wip-20260319-retry`

## Implementation Details
- **Location:** `scripts/ask_question.py`
- **Current interfaces:** `python scripts/run.py ask_question.py --question "..." [--notebook-id ID | --notebook-url URL] [--show-browser]`
- **Dependencies:** SVC_BrowserSession, AUTH_Manager (checks auth first), CONFIG_Settings (selectors, timeouts), DATA_NotebookLibrary (to resolve notebook-id to URL), SVC_NotebookManager, SVC_RetryLogic (wraps browser query block)
- **Dependents:** UTIL_RunWrapper (entry point), SVC_SkillInit (exported)

## Core Logic & Functionality
1. Resolves notebook URL from `--notebook-id` (looks up DATA_NotebookLibrary) or uses `--notebook-url` directly
2. Checks authentication via AUTH_Manager; aborts if not authenticated (non-retryable)
3. Creates `RetryHandler` from SVC_RetryLogic
4. Extracts browser block into `_do_query()` inner function; calls `handler.run(_do_query)` — full browser block is retried on transient failure
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
- Response deadline hardcoded as `time.time() + 120` (line 115) instead of using `QUERY_TIMEOUT_SECONDS` from config — changes to the config constant won't propagate; minor coupling gap

## Interface Definition

```python
# CLI:
python scripts/run.py ask_question.py \
  --question "What is the main topic?" \
  [--notebook-id <id>] \
  [--notebook-url "https://notebooklm.google.com/notebook/..."] \
  [--show-browser]

# Returns: Prints answer to stdout, exits 0 on success

# Internal usage pattern (as-built):
from retry_logic import RetryHandler, RetryExhaustedError

handler = RetryHandler()  # uses MAX_RETRIES, RETRY_BACKOFF_BASE, RATE_LIMIT_DELAY from config

def _do_query():
    """Single browser attempt: launch → navigate → query → extract."""
    playwright = sync_playwright().start()
    try:
        context = BrowserFactory.launch_persistent_context(playwright, headless=headless)
        try:
            # ... navigate, query, poll for answer ...
            if not answer:
                raise TimeoutError("Timed out waiting for NotebookLM response (120s)")
            return answer + FOLLOW_UP_REMINDER
        finally:
            context.close()
    finally:
        playwright.stop()

try:
    return handler.run(_do_query)
except RetryExhaustedError as e:
    print(f"  ❌ {e}")
    return None
```

## ARC Verification Criteria

### Functional Criteria
- [x] Given valid auth and notebook URL, returns non-empty answer
- [x] Answer contains "EXTREMELY IMPORTANT: Is that ALL you need to know?" suffix (via FOLLOW_UP_REMINDER)
- [x] `--notebook-id` correctly resolves to URL via `library.get_notebook(args.notebook_id)`
- [x] `--show-browser` makes Chrome window visible via `headless=not args.show_browser`

### Input Validation Criteria
- [x] Missing `--question` exits 1 with usage message (argparse `required=True`)
- [x] Missing notebook reference exits 1 with clear message listing available notebooks
- [x] Unauthenticated state: `ask_notebooklm()` returns None → main() prints ❌ and exits 1

### Error Handling Criteria
- [x] Transient failures (TimeoutError, RuntimeError on selector miss) raised explicitly → retried via RetryHandler
- [x] Auth check outside retry wrapper — non-retryable, returns None immediately before `handler.run()`
- [x] After retries exhausted: `RetryExhaustedError` caught, prints `❌ {e}`, returns None → exits 1
- [x] 120s deadline enforced per attempt via `time.time() + 120` (see tech debt note below)
- [x] Network errors during navigation are `Exception` subtypes → caught and retried by RetryHandler

### Quality Criteria
- [x] Nested `finally` blocks ensure `context.close()` + `playwright.stop()` after every attempt (no orphans)
- [x] All `QUERY_INPUT_SELECTORS` iterated before raising `RuntimeError`
- [x] All `RESPONSE_SELECTORS` iterated in every poll cycle before sleeping

## Future Enhancement Opportunities
- Add `--output-json` flag for structured output
- Add `--max-wait` flag to override QUERY_TIMEOUT_SECONDS per-invocation
- Cache last response to avoid re-querying identical questions
