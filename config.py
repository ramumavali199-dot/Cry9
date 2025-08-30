from datetime import time

PAIRS = [
    "BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT","BNBUSDT",
    "LTCUSDT","AVAXUSDT","LINKUSDT","ADAUSDT","DOGEUSDT",
]

SCAN_INTERVAL_MIN = 15  # minutes

CONFIDENCE_GATE = 0.65   # if mini+numeric >= 65%, then call GPT-5 final
COMPOSITE_THRESHOLD = 0.5

DEFAULT_BALANCE_USD = 10000
RISK_PER_TRADE_PCT = 0.005  # 0.5% of balance per trade
MAX_CONCURRENT_SIGNALS = 3

MIN_ATR_PCT = 0.25  # skip trades if 14-ATR% < 0.25%

LOW_TF = "15m"
HIGH_TF = "1h"

TRADING_DAYS = {0,1,2,3,4,5,6}
TRADING_WINDOW = (time(0,0), time(23,59))

MODEL_MINI = "gpt-5-mini"
MODEL_FINAL = "gpt-5"
