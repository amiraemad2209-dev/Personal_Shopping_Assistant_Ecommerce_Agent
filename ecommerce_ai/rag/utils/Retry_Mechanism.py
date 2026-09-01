
# =============================================================================
# ============================ Retry Mechanism ================================
# =============================================================================

import asyncio
import random

from rag.utils.Rate_Limite import RPMGroqRateLimiter


# HTTP errors that are usually temporary
RETRYABLE_STATUS = (429,500,502,503,504,)


async def invoke_with_retry(
    chain,
    payload: dict,
    rate_limiter: RPMGroqRateLimiter,
    run_config=None,
    max_attempts: int = 5,
):

    for attempt in range(1, max_attempts + 1):

        # Respect the RPM limit before every request
        rate_limiter.acquire()

        try:

            result = await chain.ainvoke(
                payload,
                config=run_config
            )

            return result

        except Exception as e:

            status_code = getattr(
                e,
                "status_code",
                None
            )

            # If the error is not retryable,
            # raise it immediately.
            if status_code not in RETRYABLE_STATUS:
                raise e

            # We have no attempts left
            if attempt == max_attempts:
                raise e

            # Exponential backoff:
            
            delay = min(
                (2 ** (attempt - 1)),
                60.0
            )

            # Add a small random delay
            # to avoid multiple requests retrying
            # at exactly the same time.
            jitter = random.uniform(
                0.0,
                0.3
            )

            total_delay = delay + jitter

            print(
                f"[!] Network issue "
                f"(Status {status_code}). "
                f"Retrying in "
                f"{total_delay:.2f}s..."
            )

            await asyncio.sleep(
                total_delay
            )

