import asyncio


class Scheduler:
    async def run_with_retry(self, fn, retries: int = 3, timeout: int = 30):
        for attempt in range(retries):
            try:
                return await asyncio.wait_for(fn(), timeout=timeout)
            except Exception:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2**attempt)
