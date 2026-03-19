#!/usr/bin/env python3
"""
Retry logic for NotebookLM browser automation.
Provides RetryHandler with configurable retry count, exponential backoff,
and error classification for transient vs non-retryable failures.
"""

import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import MAX_RETRIES, RETRY_BACKOFF_BASE, RATE_LIMIT_DELAY


# Signals in exception messages that indicate a rate limit
RATE_LIMIT_SIGNALS = ("rate", "quota", "429", "too many requests")

# Signals that indicate an auth error — never retry these
AUTH_SIGNALS = ("not authenticated", "authentication required", "login required", "run auth")

# Exception types that are never retried
NON_RETRYABLE_TYPES = (KeyboardInterrupt, SystemExit)


class RetryExhaustedError(Exception):
    """Raised when all retry attempts have been exhausted."""
    pass


class RetryHandler:
    """
    Retry handler for browser automation calls.

    Usage:
        handler = RetryHandler()
        result = handler.run(lambda: do_browser_work())

    On transient failure: retries with exponential backoff.
    On rate limit: waits RATE_LIMIT_DELAY seconds before retry.
    On auth error or KeyboardInterrupt: re-raises immediately.
    After max_retries exhausted: raises RetryExhaustedError.
    """

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
        last_error = None
        total_attempts = self.max_retries + 1

        for attempt in range(total_attempts):
            try:
                return func()

            except NON_RETRYABLE_TYPES:
                raise

            except Exception as e:
                msg = str(e).lower()

                # Auth errors are never retried
                if any(sig in msg for sig in AUTH_SIGNALS):
                    raise

                last_error = e

                if attempt < self.max_retries:
                    delay = self._get_delay(e, attempt)
                    print(
                        f"⚠️  Attempt {attempt + 1}/{total_attempts} failed: "
                        f"{type(e).__name__}: {e}"
                    )
                    print(f"⏳ Retrying in {delay:.1f}s...")
                    time.sleep(delay)

        raise RetryExhaustedError(
            f"All {total_attempts} attempts failed. "
            f"Last error: {type(last_error).__name__}: {last_error}"
        ) from last_error

    def _get_delay(self, exc: Exception, attempt: int) -> float:
        """Return sleep duration for this failure."""
        msg = str(exc).lower()
        if any(sig in msg for sig in RATE_LIMIT_SIGNALS):
            print(f"🚦 Rate limit detected — waiting {self.rate_limit_delay}s")
            return self.rate_limit_delay
        # Exponential backoff: 2s, 4s, 8s, ...
        return self.backoff_base ** (attempt + 1)
