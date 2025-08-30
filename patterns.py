import numpy as np
from typing import Dict

def is_bullish(o,h,l,c):
    return c>o
def is_bearish(o,h,l,c):
    return c<o

def bullish_engulfing(o1,h1,l1,c1, o2,h2,l2,c2):
    return (c2>o2) and (o2<=c1) and (c2>=o1) and (c1<o1)
def bearish_engulfing(o1,h1,l1,c1, o2,h2,l2,c2):
    return (c2<o2) and (o2>=c1) and (c2<=o1) and (c1>o1)

def hammer(o,h,l,c):
    body = abs(c-o)
    lower = o-l if c>=o else c-l
    upper = h-c if c>=o else h-o
    return (lower>=2*body) and (upper<=body)

def shooting_star(o,h,l,c):
    body = abs(c-o)
    upper = h-c if c>=o else h-o
    lower = o-l if c>=o else c-l
    return (upper>=2*body) and (lower<=body)

def pattern_signal(o,h,l,c) -> Dict[str,bool]:
    if len(o)<2:
        return {"bull_engulf":False, "bear_engulf":False, "hammer":False, "shooting_star":False}
    o1,h1,l1,c1 = o[-2],h[-2],l[-2],c[-2]
    o2,h2,l2,c2 = o[-1],h[-1],l[-1],c[-1]
    return {
        "bull_engulf": bullish_engulfing(o1,h1,l1,c1,o2,h2,l2,c2),
        "bear_engulf": bearish_engulfing(o1,h1,l1,c1,o2,h2,l2,c2),
        "hammer": hammer(o2,h2,l2,c2),
        "shooting_star": shooting_star(o2,h2,l2,c2)
    }

def channel_breakout(c, window=20, tolerance=0.0015):
    if len(c)<window+1:
        return {"breakout_up":False, "breakout_down":False}
    recent = c[-window-1:-1]
    lo, hi = np.min(recent), np.max(recent)
    last = c[-1]
    brk_up = last > hi*(1+tolerance)
    brk_dn = last < lo*(1-tolerance)
    return {"breakout_up": brk_up, "breakout_down": brk_dn}
