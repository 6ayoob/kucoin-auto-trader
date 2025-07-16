import os
import csv
from kucoin.client import Client
from config import KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE, TRADE_PERCENT, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT
from telegram_bot import send_message

client = Client(KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE)

def get_usdt_balance():
    accounts = client.get_accounts()
    for acc in accounts:
        if acc['currency'] == 'USDT' and acc['type'] == 'trade':
            return float(acc['available'])
    return 0.0

def get_current_price(symbol):
    return float(client.get_ticker(symbol)['price'])

def calculate_quantity(symbol, usdt_balance):
    price = get_current_price(symbol)
    amount = (usdt_balance * TRADE_PERCENT / 100) / price
    return round(amount, 4)

def execute_buy(symbol):
    usdt_balance = get_usdt_balance()
    if usdt_balance < 5:
        send_message("❌ لا يوجد رصيد كافٍ للشراء.")
        return
    qty = calculate_quantity(symbol, usdt_balance)
    try:
        order = client.create_market_order(symbol, 'buy', size=str(qty))
        price = get_current_price(symbol)
        log_trade(symbol, 'BUY', qty, price)
        send_message(f"✅ تم تنفيذ عملية شراء لـ {symbol} بسعر {price}")
    except Exception as e:
        send_message(f"❌ فشل في تنفيذ الشراء: {e}")

def execute_sell(symbol, qty, buy_price):
    try:
        order = client.create_market_order(symbol, 'sell', size=str(qty))
        price = get_current_price(symbol)
        profit = ((price - buy_price) / buy_price) * 100
        log_trade(symbol, 'SELL', qty, price, profit)
        send_message(f"📤 تم بيع {symbol} بسعر {price}\nالربح: {round(profit, 2)}٪")
    except Exception as e:
        send_message(f"❌ فشل في تنفيذ البيع: {e}")

def should_take_profit_or_stop_loss(current_price, buy_price):
    change = ((current_price - buy_price) / buy_price) * 100
    if change <= -STOP_LOSS_PERCENT:
        return 'stop_loss'
    if change >= TAKE_PROFIT_PERCENT:
        return 'take_profit'
    return None

def log_trade(symbol, side, qty, price, profit=None):
    file_exists = os.path.isfile('trades.csv')
    with open('trades.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['symbol', 'side', 'qty', 'price', 'profit'])
        writer.writerow([symbol, side, qty, price, profit])
