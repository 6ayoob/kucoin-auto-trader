import pandas as pd

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices):
    ema12 = prices.ewm(span=12, adjust=False).mean()
    ema26 = prices.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def is_entry_signal(prices):
    ma50 = prices.rolling(window=50).mean()
    rsi = calculate_rsi(prices)
    macd, signal = calculate_macd(prices)

    latest_close = prices.iloc[-1]
    latest_ma50 = ma50.iloc[-1]
    latest_rsi = rsi.iloc[-1]
    latest_macd = macd.iloc[-1]
    latest_signal = signal.iloc[-1]

    return (
        latest_close > latest_ma50 and
        40 < latest_rsi < 70 and
        latest_macd > latest_signal
    )
