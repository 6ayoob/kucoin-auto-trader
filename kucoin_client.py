import ccxt
from config import KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE

exchange = ccxt.kucoin({
    'apiKey': KUCOIN_API_KEY,
    'secret': KUCOIN_API_SECRET,
    'password': KUCOIN_API_PASSPHRASE,
    'enableRateLimit': True,
})

def fetch_balance():
    return exchange.fetch_free_balance()

def create_market_order(symbol, side, amount):
    return exchange.create_market_order(symbol, side, amount)

def fetch_ohlcv(symbol, timeframe='1m', limit=100):
    return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)