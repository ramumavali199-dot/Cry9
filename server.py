from flask import Flask
import threading
import asyncio
import main  # import main.py directly

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_bot():
    if hasattr(main, "main"):
        if asyncio.iscoroutinefunction(main.main):
            asyncio.run(main.main())   # async main
        else:
            main.main()                # normal main
    else:
        import importlib
        importlib.reload(main)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)
