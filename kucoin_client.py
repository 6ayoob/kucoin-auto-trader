import time
import requests
import pandas as pd
from kucoin.client import Client
from strategies import apply_strategy
from telegram_bot import send_telegram_message
from config import KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE

client = Client(KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE)

SYMBOL = "BTC-USDT"
TRADE_AMOUNT = 5

def fetch_ohlcv(symbol, interval='1h', limit=100):
    url = f'https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}'
    data = requests.get(url).json()['data']
    df = pd.DataFrame(data, columns=['time', 'open', 'close', 'high', 'low', 'volume', 'turnover'])
    df = df.astype(float).iloc[::-1]
    return df

def execute_trade(signal):
    if signal == "buy":
        client.create_market_order(SYMBOL, 'buy', funds=str(TRADE_AMOUNT))
        send_telegram_message(f"✅ شراء {SYMBOL} بمبلغ {TRADE_AMOUNT}$")
    elif signal == "sell":
        balance = client.get_account_list(type="trade", currency="BTC")
        qty = float(balance[0]['available'])
        if qty > 0.0001:
            client.create_market_order(SYMBOL, 'sell', size=str(qty))
            send_telegram_message(f"🚨 بيع {qty} من {SYMBOL}")

def start_trading_bot():
    while True:
        try:
            df = fetch_ohlcv(SYMBOL)
            signal = apply_strategy(df)
            send_telegram_message(f"📊 إشارة التداول: {signal}")
            execute_trade(signal)
        except Exception as e:
            send_telegram_message(f"❌ خطأ: {e}")
        time.sleep(3600)
