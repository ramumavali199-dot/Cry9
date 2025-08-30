import asyncio
import aiohttp
from typing import List, Dict, Any

BINANCE_BASE = "https://api.binance.com"

async def fetch_klines(session: aiohttp.ClientSession, symbol: str, interval: str = "15m", limit: int = 200) -> List[List[Any]]:
    url = f"{BINANCE_BASE}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    async with session.get(url, timeout=15) as r:
        r.raise_for_status()
        return await r.json()

async def fetch_book_ticker(session: aiohttp.ClientSession, symbol: str) -> Dict[str, Any]:
    url = f"{BINANCE_BASE}/api/v3/ticker/bookTicker?symbol={symbol}"
    async with session.get(url, timeout=10) as r:
        r.raise_for_status()
        return await r.json()

async def fetch_oi_placeholder(session: aiohttp.ClientSession, symbol: str) -> float:
    url = f"{BINANCE_BASE}/api/v3/ticker/24hr?symbol={symbol}"
    async with session.get(url, timeout=10) as r:
        r.raise_for_status()
        data = await r.json()
        try:
            return float(data.get("quoteVolume", 0.0))
        except Exception:
            return 0.0

async def gather_market_snapshot(symbols: List[str], low_tf: str, high_tf: str, session: aiohttp.ClientSession):
    tasks = []
    for s in symbols:
        tasks.append(fetch_klines(session, s, interval=low_tf, limit=200))
        tasks.append(fetch_klines(session, s, interval=high_tf, limit=200))
        tasks.append(fetch_book_ticker(session, s))
        tasks.append(fetch_oi_placeholder(session, s))
    res = await asyncio.gather(*tasks, return_exceptions=True)
    out = {}
    i = 0
    for s in symbols:
        kl_low = res[i]; i+=1
        kl_high = res[i]; i+=1
        book = res[i]; i+=1
        oi = res[i]; i+=1
        out[s] = {"klines_low": kl_low, "klines_high": kl_high, "book": book, "oi_proxy": oi}
    return out
