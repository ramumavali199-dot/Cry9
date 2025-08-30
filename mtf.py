from indicators import ema
import numpy as np

def trend_bias(close_low_tf, close_high_tf) -> str:
    e8_l = ema(close_low_tf,8)
    e21_l = ema(close_low_tf,21)
    e8_h = ema(close_high_tf,8)
    e21_h = ema(close_high_tf,21)
    bull = (e8_l[-1]>e21_l[-1]) and (e8_h[-1]>e21_h[-1])
    bear = (e8_l[-1]<e21_l[-1]) and (e8_h[-1]<e21_h[-1])
    if bull: return "bull"
    if bear: return "bear"
    return "neutral"
