import os
from typing import Dict
from datetime import datetime, timezone
from telegram import Bot

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None

def send_alert(payload: Dict):
    if not bot or not CHAT_ID:
        print("[ALERT]", payload)
        return
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text = (
        f"🚨[CRYPTO SIGNAL]\n"
        f"Pair: {payload.get('symbol')}\n"
        f"Bias: {payload.get('bias').upper()}\n"
        f"Entry: {payload.get('entry_price')} | SL%: {payload.get('stop_loss_pct')} | TP%: {payload.get('target_pct')}\n"
        f"Size: ${payload.get('size_usd')} | Conf: {int(payload.get('confidence',0)*100)}%\n"
        f"Reason: {payload.get('reason')}\n"
        f"Time: {ts}\n\n"
        f"JSON: {payload}"
    )
    bot.send_message(chat_id=CHAT_ID, text=text)
