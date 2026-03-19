# SVC_AskQuestion.md

## Purpose
Core query engine. Opens a browser session to the specified NotebookLM notebook, types the user's question into the query input, waits for Gemini's streaming response to stabilize, extracts the answer text from the DOM, and returns it. This is the primary value-delivery component of the skill.

## Current Implementation Status
✅ **IMPLEMENTED** — Component exists and is functional

## Implementation Details
- **Location:** `scripts/ask_question.py`
- **Current interfaces:** `python scripts/run.py ask_question.py --question "..." [--notebook-id ID | --notebook-url URL] [--show-browser]`
- **Dependencies:** SVC_BrowserSession, AUTH_Manager (checks auth first), CONFIG_Settings (selectors, timeouts), DATA_NotebookLibrary (to resolve notebook-id to URL), SVC_NotebookManager
- **Dependents:** UTIL_RunWrapper (entry point), SVC_SkillInit (exported)

## Core Logic & Functionality
1. Resolves notebook URL from `--notebook-id` (looks up DATA_NotebookLibrary) or uses `--notebook-url` directly
2. Checks authentication via AUTH_Manager; aborts if not authenticated
3. Opens SVC_BrowserSession (authenticated Chrome)
4. Navigates to the notebook URL
5. Waits for page load (PAGE_LOAD_TIMEOUT = 30s)
6. Locates query input via QUERY_INPUT_SELECTORS (tries each selector in order)
7. Types question with human-like timing (StealthUtils typing speed simulation)
8. Submits query (Enter key)
9. Waits for response to appear via RESPONSE_SELECTORS
10. Detects streaming completion (response stops growing for N consecutive checks)
11. Extracts and returns full response text
12. Appends follow-up prompt: "EXTREMELY IMPORTANT: Is that ALL you need to know?"

## Current Quality Assessment
- **Completeness:** Fully functional for standard queries; handles English and German NotebookLM UI
- **Code Quality:** Solid async implementation with selector fallbacks
- **Test Coverage:** No automated tests; extensively tested manually
- **Documentation:** SKILL.md covers all CLI options; references/usage_patterns.md covers best practices

## Technical Debt & Improvement Areas
- Single retry on selector failure; should use SVC_RetryLogic (missing) for robust retry
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
- [ ] Selector not found after timeout exits 1 with diagnostic message
- [ ] QUERY_TIMEOUT_SECONDS (120s) respected; exits cleanly on timeout
- [ ] Network errors during navigation handled gracefully

### Quality Criteria
- [ ] Chrome process closed after each query (no orphans)
- [ ] Both QUERY_INPUT_SELECTORS tried before failing
- [ ] Both RESPONSE_SELECTORS tried before failing

## Future Enhancement Opportunities
- Integrate with SVC_RetryLogic for automatic retry on transient failures
- Add `--output-json` flag for structured output
- Add `--max-wait` flag to override QUERY_TIMEOUT_SECONDS per-invocation
- Cache last response to avoid re-querying identical questions
