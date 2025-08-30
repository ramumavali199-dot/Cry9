import os
import asyncio
import numpy as np
from typing import Dict, Any

from config import PAIRS, SCAN_INTERVAL_MIN, LOW_TF, HIGH_TF, MIN_ATR_PCT, COMPOSITE_THRESHOLD, CONFIDENCE_GATE, RISK_PER_TRADE_PCT, DEFAULT_BALANCE_USD, MAX_CONCURRENT_SIGNALS
from data_sources import gather_market_snapshot
from indicators import ohlcv_from_klines, atr_pct, momentum
from patterns import pattern_signal, channel_breakout
from mtf import trend_bias
from scoring import pattern_score, mtf_score, combine_scores
from openai_adapter import mini_sentiment, final_decision
from telegram_alerts import send_alert
from scheduler import run_every
import aiohttp

async def single_scan():
    async with aiohttp.ClientSession() as session:
        snap = await gather_market_snapshot(PAIRS, LOW_TF, HIGH_TF, session)

    signals = []
    for sym in PAIRS:
        data = snap.get(sym)
        if not data: continue
        try:
            o_l,h_l,l_l,c_l,v_l = ohlcv_from_klines(data["klines_low"])
            o_h,h_h,l_h,c_h,v_h = ohlcv_from_klines(data["klines_high"])
        except Exception:
            continue

        atrp = atr_pct(h_l,l_l,c_l)
        if atrp < MIN_ATR_PCT:
            continue

        pflags = pattern_signal(o_l,h_l,l_l,c_l)
        ch = channel_breakout(c_l)
        patt = pattern_score(pflags)
        if ch["breakout_up"]: patt = max(patt, 0.7)
        if ch["breakout_down"]: patt = min(patt, -0.7)

        mom = momentum(c_l, lookback=10)
        mom_score = float(np.tanh(mom*5))

        mtf = mtf_score(trend_bias(c_l, c_h))

        vol_proxy = 0.0
        try:
            vol_proxy = float(data["book"].get("bidQty", 0)) - float(data["book"].get("askQty", 0))
        except Exception:
            pass
        oi_proxy = data.get("oi_proxy", 0.0)

        oi_s = 0.0 if oi_proxy==0 else float(np.tanh(np.log10(oi_proxy+1e-6)/6))
        vol_s = float(np.tanh(vol_proxy/1000))

        parts = {
            "pattern": patt,
            "momentum": mom_score,
            "oi": oi_s,
            "volume": vol_s,
            "mtf": mtf,
        }
        numeric_score = combine_scores(parts)

        if abs(numeric_score) < 0.35:
            continue

        headlines = [f"{sym} placeholder headline 1", f"{sym} placeholder headline 2"]
        mini = mini_sentiment(sym, {"numeric_score":numeric_score, "atr_pct":atrp}, headlines)
        news_s = float(mini.get("news_sentiment", 0.0))

        final_composite = combine_scores({**parts, "news": news_s})
        direction = "long" if final_composite>=COMPOSITE_THRESHOLD else ("short" if final_composite<=-COMPOSITE_THRESHOLD else "neutral")
        if direction == "neutral":
            continue

        confidence = min(1.0, max(0.0, abs(final_composite)))
        if confidence < CONFIDENCE_GATE:
            continue

        payload = {
            "symbol": sym,
            "timeframe": LOW_TF,
            "numeric": {
                "numeric_score": round(numeric_score,3),
                "final_composite": round(final_composite,3),
                "atr_pct": round(atrp,3),
                "momentum": round(mom,5),
                "oi_proxy": oi_proxy,
                "volume_proxy": vol_proxy,
                "mtf": mtf,
            },
            "news": mini,
            "direction_hint": direction,
            "account": {"balance_usd": float(os.getenv("ACCOUNT_BALANCE_USD", DEFAULT_BALANCE_USD)), "risk_per_trade_pct": float(os.getenv("RISK_PER_TRADE_PCT", RISK_PER_TRADE_PCT))}
        }
        decision = final_decision(payload)

        bias = decision.get("suggested_bias", direction)
        sl_pct = float(decision.get("stop_loss_pct", 1.5))
        tp_pct = float(decision.get("target_pct", 2.0))
        conf = float(decision.get("confidence", confidence))

        balance = float(os.getenv("ACCOUNT_BALANCE_USD", DEFAULT_BALANCE_USD))
        risk_pct = float(os.getenv("RISK_PER_TRADE_PCT", RISK_PER_TRADE_PCT))
        risk_usd = balance * risk_pct * conf
        entry_price = decision.get("entry_price")
        if entry_price is None:
            entry_price = float(c_l[-1])
        sl_distance = max(0.001, sl_pct/100.0)
        size_usd = risk_usd / sl_distance

        reason = decision.get("one_line_rationale", "numeric + news composite")
        signals.append({
            "symbol": sym,
            "bias": bias,
            "entry_price": round(entry_price, 4),
            "stop_loss_pct": round(sl_pct, 3),
            "target_pct": round(tp_pct, 3),
            "size_usd": round(size_usd, 2),
            "confidence": round(conf, 3),
            "reason": reason,
        })

        if len(signals) >= MAX_CONCURRENT_SIGNALS:
            break

    for s in signals:
        send_alert(s)

async def main():
    await run_every(SCAN_INTERVAL_MIN, single_scan)

if __name__ == "__main__":
    asyncio.run(main())
