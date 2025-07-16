from kucoin.client import Client
import time
from config import KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE, SYMBOLS, TRADE_PERCENT, STOP_LOSS_PERCENT
from strategies import should_buy, should_sell
from telegram_bot import send_telegram_message

client = Client(KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE)

def run_trading_bot():
    send_telegram_message("🚀 البوت بدأ العمل الآن ✅")

    while True:
        for symbol in SYMBOLS:
            try:
                klines = client.get_kline(symbol, kline_type="1min", limit=100)
                closes = [float(c[2]) for c in klines]
                current_price = closes[-1]

                balance = client.get_account_list()
                usdt_balance = float(next((b['balance'] for b in balance if b['currency'] == 'USDT' and b['type'] == 'trade'), "0"))

                qty = (usdt_balance * TRADE_PERCENT / 100) / current_price

                if should_buy(closes):
                    order = client.create_market_order(symbol, 'buy', size=round(qty, 6))
                    send_telegram_message(f"✅ شراء {symbol} بسعر {current_price}")
                elif should_sell(closes):
                    send_telegram_message(f"📉 إشارة بيع لـ {symbol} (اختبار فقط)")
            except Exception as e:
                send_telegram_message(f"❌ خطأ في التداول لـ {symbol}: {str(e)}")

        time.sleep(300)  # كل 5 دقائق
