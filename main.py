import threading
from kucoin_client import start_trading_bot

def run_bot():
    start_trading_bot()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    from app import app
    app.run(host="0.0.0.0", port=10000)
