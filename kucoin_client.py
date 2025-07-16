from kucoin.client import Client
from config import KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE

client = Client(KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE)

def start_trading_bot():
    print("✅ Kucoin spot client initialized.")
    # لاحقًا: ضع هنا منطق التداول الفعلي
