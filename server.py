from flask import Flask
import threading
import main  # import main.py directly (no src folder)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_bot():
    if hasattr(main, "main"):
        main.main()
    else:
        import importlib
        importlib.reload(main)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)
