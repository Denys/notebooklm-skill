# SVC_RetryLogic.md

## Purpose
Dedicated retry and recovery service for browser automation failures. Provides a `RetryHandler` sync context manager that wraps any code block with configurable retry count, exponential backoff, and error classification — distinguishing transient failures (timeout, selector miss, rate limit) from non-retryable ones (auth failure, invalid URL). Used by SVC_AskQuestion to wrap the full browser launch → navigate → query → extract cycle.

## Current Implementation Status
🟢 **VERIFIED** — `wip-20260319-retry`

## MVP Context
- **Required for Feature:** Reliable query execution (Browser Automation)
- **Priority:** High — affects core reliability of every query
- **Blocking:** Nothing currently blocked (SVC_AskQuestion works without it, but fails silently on transient errors)

## Implementation Details
- **Location:** `scripts/retry_logic.py`
- **Current interfaces:** `RetryHandler` class; used as a sync context manager via `with handler.attempt():`
- **Dependencies:** `CONFIG_Settings` (MAX_RETRIES, RETRY_BACKOFF_BASE, RATE_LIMIT_DELAY constants)
- **Dependents:** `SVC_AskQuestion` (wraps full query block)

## Core Logic & Functionality

### Error Classification
RetryHandler classifies failures into four categories:

| Category | Detection | Action |
|----------|-----------|--------|
| **Timeout** | `TimeoutError` or "timeout" in message | Retry with exponential backoff |
| **Rate limit** | "rate" / "quota" / "429" in message | Wait `RATE_LIMIT_DELAY` seconds, then retry |
| **Selector miss** | `SelectorNotFoundError` or "selector" in message | Retry with exponential backoff |
| **Non-retryable** | Auth errors, `KeyboardInterrupt`, `SystemExit` | Re-raise immediately, no retry |
| **Generic crash** | Any other `Exception` | Retry with exponential backoff |

### Retry Sequence
1. Execute the wrapped block
2. On exception: classify the error
3. If non-retryable: re-raise immediately
4. If retryable and attempts remaining: print attempt message, sleep (backoff or fixed delay), loop
5. If retryable and max attempts exhausted: raise `RetryExhaustedError` with full diagnostic context
6. On success: return normally

### Backoff Formula
```
sleep_seconds = backoff_base ** attempt_number
# attempt 1 → 2.0s, attempt 2 → 4.0s, attempt 3 → 8.0s
```
Rate-limit waits use `RATE_LIMIT_DELAY` (fixed, not exponential).

### Output During Retry
Each retry attempt prints:
```
⚠️  Attempt 1/3 failed: <error summary>
⏳ Retrying in 2.0s...
```
Final failure prints:
```
❌ All 3 attempts failed. Last error: <error>
```

## Interface Definition

```python
# scripts/retry_logic.py

import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import MAX_RETRIES, RETRY_BACKOFF_BASE, RATE_LIMIT_DELAY


RATE_LIMIT_SIGNALS = ("rate", "quota", "429", "too many requests")
AUTH_SIGNALS = ("not authenticated", "authentication required", "login required", "run auth")
NON_RETRYABLE_TYPES = (KeyboardInterrupt, SystemExit)


class RetryExhaustedError(Exception):
    """Raised when all retry attempts have been exhausted."""
    pass


class RetryHandler:
    def __init__(
        self,
        max_retries: int = MAX_RETRIES,
        backoff_base: float = RETRY_BACKOFF_BASE,
        rate_limit_delay: float = RATE_LIMIT_DELAY,
    ):
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.rate_limit_delay = rate_limit_delay

    def run(self, func):
        """
        Call func(), retrying on transient errors.

        Args:
            func: Zero-argument callable to execute with retry.

        Returns:
            The return value of func() on success.

        Raises:
            RetryExhaustedError: When all attempts fail.
            Original exception: For non-retryable errors (auth, KeyboardInterrupt).
        """
        ...

    def _get_delay(self, exc: Exception, attempt: int) -> float:
        """Return sleep duration: RATE_LIMIT_DELAY for rate limits, backoff_base**(attempt+1) otherwise."""
        ...


# Intended usage in SVC_AskQuestion:
#
#   handler = RetryHandler()
#   return handler.run(_do_query)   # _do_query is a zero-arg callable
```

## ARC Verification Criteria

### Functional Criteria
- [x] Retries up to `max_retries` times on transient errors (TimeoutError, generic Exception)
- [x] Exponential backoff sleep applied between retries (`backoff_base ** (attempt + 1)` → 2.0s, 4.0s, 8.0s)
- [x] Rate limit signals trigger `RATE_LIMIT_DELAY` fixed wait instead of backoff
- [x] Raises `RetryExhaustedError` after max attempts exhausted, preserving last exception via `raise ... from last_error`
- [x] Returns normally (no exception) when wrapped block succeeds on any attempt

### Input Validation Criteria
- [x] `max_retries=0` → total_attempts=1; immediate `RetryExhaustedError` on first failure, no sleep
- [x] `max_retries=1` → total_attempts=2; one retry attempt with one backoff sleep before second attempt
- [x] Constructor defaults match CONFIG_Settings constants (MAX_RETRIES=3, RETRY_BACKOFF_BASE=2.0, RATE_LIMIT_DELAY=45)

### Error Handling Criteria
- [x] `KeyboardInterrupt` and `SystemExit` re-raised immediately via `except NON_RETRYABLE_TYPES: raise`
- [x] Auth error signals ("not authenticated", "authentication required", "login required", "run auth") re-raised immediately
- [x] `RetryExhaustedError` message includes attempt count and last error text: `"All {n} attempts failed. Last error: {Type}: {msg}"`

### Quality Criteria
- [x] Non-final failed attempts print `⚠️ Attempt N/M failed: Type: msg` + `⏳ Retrying in Xs...`
- [x] No infinite loop possible — hard ceiling at `range(max_retries + 1)`
- [x] Pure Python stdlib — `time`, `sys`, `pathlib` only; no new dependencies beyond `config.py`
- [x] Works with `sync_playwright` (synchronous `time.sleep`, not async)

## Implementation Notes

### Recommended Implementation Pattern
The cleanest sync retry pattern for `ask_question.py` integration:

```python
class RetryHandler:
    @contextmanager
    def attempt(self):
        last_error = None
        for i in range(self.max_retries + 1):
            try:
                yield  # caller's block runs here
                return  # success — exit
            except NON_RETRYABLE:
                raise
            except Exception as e:
                last_error = e
                if i == self.max_retries:
                    break
                delay = self._classify_delay(e, i)
                print(f"⚠️  Attempt {i+1}/{self.max_retries+1} failed: {e}")
                print(f"⏳ Retrying in {delay:.1f}s...")
                time.sleep(delay)
        raise RetryExhaustedError(
            f"All {self.max_retries+1} attempts failed. Last: {last_error}"
        ) from last_error
```

> **Note:** A `@contextmanager` that `yield`s inside a loop and catches exceptions around the yield is the correct stdlib pattern for this use case. The `yield` transfers control to the `with` block; exceptions propagate back into the generator where they are caught.

### Auth Error Detection
Auth errors must not be retried. Detect via message content:
```python
msg = str(e).lower()
if any(sig in msg for sig in AUTH_SIGNALS):
    raise  # immediate re-raise
```

### Integration Point in ask_question.py
The retry wraps the entire browser block (playwright start → context → navigate → query → extract):
```python
handler = RetryHandler()
with handler.attempt():
    playwright = sync_playwright().start()
    # ... full query flow ...
    answer = _extract_answer(page)
```
The `finally` block (context.close, playwright.stop) remains outside the retry wrapper to ensure cleanup always runs.
