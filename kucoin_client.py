from kucoin.client import Client
from strategies import should_buy, should_sell
from telegram_bot import send_telegram_message
import time

# إعدادات API ومحددات التداول
KUCOIN_API_KEY = "63c38cd705a0c50001e97849"
KUCOIN_API_SECRET = "1e3f4e7a-78f8-48b1-a3b4-6f7b5e15f49b"
KUCOIN_API_PASSPHRASE = "zidni123"
STOP_LOSS_PERCENT = 5  # نسبة الإيقاف

client = Client(KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE)


def get_usdt_symbols():
    """جلب جميع رموز العملات مقابل USDT"""
    symbols = client.get_symbol_list()
    return [s["symbol"] for s in symbols if s["quoteCurrency"] == "USDT" and s["enableTrading"]]


def check_market(symbol="BTC-USDT"):
    """تحليل السوق لعملة واحدة"""
    try:
        klines = client.get_kline_data(symbol, kline_type="15min", limit=50)
        closes = [float(k[2]) for k in klines]  # سعر الإغلاق
        last_price = float(client.get_ticker(symbol)["price"])

        market_data = {
            "closes": closes,
            "price": last_price
        }

        if should_buy(market_data):
            send_telegram_message(f"📈 فرصة شراء محتملة لـ {symbol} عند السعر: {last_price}")

        buy_price = 51000  # مثال، يجب استبداله بالسعر الفعلي للشراء
        if should_sell(market_data, buy_price, STOP_LOSS_PERCENT):
            send_telegram_message(f"⚠️ إشارة بيع لـ {symbol} - كسر الستوب لوز. السعر الحالي: {last_price}")

    except Exception as e:
        send_telegram_message(f"❌ خطأ أثناء تحليل {symbol}: {str(e)}")


def check_all_usdt_pairs():
    """تحليل جميع العملات مقابل USDT"""
    symbols = get_usdt_symbols()
    send_telegram_message(f"🔍 بدء تحليل {len(symbols)} عملة...")
    for symbol in symbols:
        time.sleep(0.5)  # لتقليل الضغط على API
        check_market(symbol)
