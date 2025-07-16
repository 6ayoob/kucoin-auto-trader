import ccxt
import pandas as pd
import ta

client = ccxt.kucoin()

def fetch_ohlcv(symbol, timeframe='1m', limit=100):
    return client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

def get_indicators(symbol):
    ohlcv = fetch_ohlcv(symbol)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['EMA10'] = ta.trend.ema_indicator(df['close'], window=10).ema_indicator()
    df['EMA50'] = ta.trend.ema_indicator(df['close'], window=50).ema_indicator()
    df['RSI'] = ta.momentum.RSIIndicator(df['close']).rsi()
    macd = ta.trend.MACD(df['close'])
    df['MACD'] = macd.macd()
    df['Signal'] = macd.macd_signal()
    return df

def should_buy(symbol):
    df = get_indicators(symbol).dropna()
    if df.empty: return False
    latest = df.iloc[-1]
    return latest['EMA10'] > latest['EMA50'] and latest['RSI'] < 70 and latest['MACD'] > latest['Signal']

def should_sell(symbol):
    df = get_indicators(symbol).dropna()
    if df.empty: return False
    latest = df.iloc[-1]
    return latest['EMA10'] < latest['EMA50'] or latest['MACD'] < latest['Signal']