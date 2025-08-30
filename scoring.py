from typing import Dict
import numpy as np

WEIGHTS = {
    "pattern": 0.25,
    "momentum": 0.20,
    "oi": 0.15,
    "volume": 0.10,
    "mtf": 0.15,
    "news": 0.15,
}

def normalize(x, lo=-1, hi=1):
    if x is None:
        return 0.0
    return max(min(x,hi),lo)

def pattern_score(flags: Dict[str,bool]) -> float:
    if flags.get("bull_engulf"): return 1.0
    if flags.get("bear_engulf"): return -1.0
    if flags.get("hammer"): return 0.6
    if flags.get("shooting_star"): return -0.6
    return 0.0

def mtf_score(bias: str) -> float:
    return {"bull":1.0, "bear":-1.0}.get(bias, 0.0)

def combine_scores(parts: Dict[str,float]) -> float:
    total = 0.0
    wsum = 0.0
    for k,v in parts.items():
        w = WEIGHTS.get(k,0.0)
        total += w*normalize(v)
        wsum += w
    return total/wsum if wsum else 0.0
