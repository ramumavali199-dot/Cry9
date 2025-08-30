# Crypto Signal Bot (Koyeb 512MB Ready)

Scans 10 crypto pairs every 15 minutes using Candlesticks + Patterns (entry idea), OI & Volume (confirmation), News/Sentiment via GPT-5-mini, and final Entry/SL/Target via GPT-5 when confidence ≥ 65%. Adds MTF check (15m vs 1h), volatility filter (ATR), and position sizing with fixed risk %.

## Quick start
1) Put your keys in Koyeb Service → Environment:
   - TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
   - OPENAI_API_KEY
   - RISK_PER_TRADE_PCT (e.g., 0.005 for 0.5%)
   - MAX_CONCURRENT_SIGNALS (e.g., 3)
2) Deploy via Git public repo in Koyeb with Dockerfile.
3) Edit pairs in `config.py` if needed.

Run locally:
```bash
pip install -r requirements.txt
python -m src.main
```
