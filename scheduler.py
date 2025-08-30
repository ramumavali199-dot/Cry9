import asyncio
from datetime import datetime, timezone

async def run_every(minutes: int, coro_func, *args, **kwargs):
    while True:
        start = datetime.now(timezone.utc)
        try:
            await coro_func(*args, **kwargs)
        except Exception as e:
            print("[loop_error]", e)
        elapsed = (datetime.now(timezone.utc)-start).total_seconds()
        wait = max(0, minutes*60 - elapsed)
        await asyncio.sleep(wait)
