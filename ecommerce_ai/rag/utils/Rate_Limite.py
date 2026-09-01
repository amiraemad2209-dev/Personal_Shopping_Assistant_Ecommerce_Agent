

# =============================================================================
# ========================== Groq Rate Limiter ================================
# =============================================================================

import time
import threading
from collections import deque


class RPMGroqRateLimiter:

    def __init__(
        self,
        rpm: int = 30,
        window_s: float = 60.0
    ):
        self.rpm = rpm
        self.window_s = window_s

        # Store timestamps of recent requests
        self._req_timestamps = deque()

        # Protect the queue when multiple requests happen
        # at the same time.
        self._lock = threading.Lock()


    def _purge_expired(self, now: float) -> None:

        cutoff = now - self.window_s

        while (
            self._req_timestamps
            and self._req_timestamps[0] < cutoff
        ):
            self._req_timestamps.popleft()


    def acquire(self, timeout: float = 90.0) -> bool:

        deadline = time.monotonic() + timeout

        while True:

            with self._lock:

                now = time.monotonic()

                # Remove requests older than 60 seconds
                self._purge_expired(now)

                # We still have room for another request
                if len(self._req_timestamps) < self.rpm:

                    self._req_timestamps.append(now)

                    return True

            # We reached the RPM limit
            if time.monotonic() > deadline:

                raise TimeoutError(
                    "Rate limit acquire timed out"
                )

            # Wait before checking again
            time.sleep(0.5)

