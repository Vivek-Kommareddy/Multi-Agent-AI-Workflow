import asyncio
import logging

logger = logging.getLogger(__name__)


class Scheduler:
    async def run_with_retry(self, fn, retries: int = 3, timeout: int = 30):
        for attempt in range(retries):
            try:
                return await asyncio.wait_for(fn(), timeout=timeout)
            except Exception as exc:
                if attempt == retries - 1:
                    logger.error(
                        "All %d retry attempts exhausted. Last error: %s",
                        retries,
                        exc,
                        exc_info=True,
                    )
                    raise
                wait = 2 ** attempt
                logger.warning(
                    "Attempt %d/%d failed (%s: %s). Retrying in %ds...",
                    attempt + 1,
                    retries,
                    type(exc).__name__,
                    exc,
                    wait,
                )
                await asyncio.sleep(wait)
