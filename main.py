import time
import pandas as pd
from kucoin_client import fetch_balance, create_market_order, fetch_ohlcv
from strategies import analyze
from config import TRADE_PERCENT
from telegram_bot import send_telegram

symbol = "BTC/USDT"
timeframe = '1m'

def run_bot():
    try:
        ohlcv = fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        if analyze(df):
            balance = fetch_balance()
            usdt = balance.get('USDT', 0)
            if usdt > 10:
                amount = (usdt * TRADE_PERCENT / 100) / df['close'].iloc[-1]
                order = create_market_order(symbol, 'buy', amount)
                msg = f"🚀 شراء {symbol}\nالسعر: {df['close'].iloc[-1]:.2f}\nالكمية: {amount:.6f}"
                send_telegram(msg)
    except Exception as e:
        send_telegram(f"❌ خطأ في البوت:\n{str(e)}")

while True:
    run_bot()
    time.sleep(60)