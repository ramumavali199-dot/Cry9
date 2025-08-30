from typing import List, Tuple
import numpy as np

def to_float(arr):
    return np.array(arr, dtype=float)

def ohlcv_from_klines(kl):
    o = to_float([x[1] for x in kl])
    h = to_float([x[2] for x in kl])
    l = to_float([x[3] for x in kl])
    c = to_float([x[4] for x in kl])
    v = to_float([x[5] for x in kl])
    return o,h,l,c,v

def ema(arr: np.ndarray, span: int) -> np.ndarray:
    k = 2/(span+1)
    ema_vals = np.zeros_like(arr)
    ema_vals[0] = arr[0]
    for i in range(1,len(arr)):
        ema_vals[i] = arr[i]*k + ema_vals[i-1]*(1-k)
    return ema_vals

def atr(h,l,c, period=14) -> float:
    tr = np.maximum(h[1:] - l[1:], np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
    if len(tr) < period:
        return float(np.mean(tr)) if len(tr)>0 else 0.0
    return float(np.mean(tr[-period:]))

def atr_pct(h,l,c) -> float:
    _atr = atr(h,l,c,14)
    last_close = c[-1]
    return (_atr/last_close)*100 if last_close else 0.0

def momentum(c, lookback=10) -> float:
    if len(c) < lookback+1:
        return 0.0
    return float((c[-1]-c[-1-lookback])/c[-1-lookback])
