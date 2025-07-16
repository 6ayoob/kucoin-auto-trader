import pandas as pd
from ta.momentum import RSIIndicator

def calculate_macd(close_prices, short_window=12, long_window=26, signal_window=9):
    short_ema = close_prices.ewm(span=short_window, adjust=False).mean()
    long_ema = close_prices.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def calculate_rsi(close_prices, period=14):
    rsi = RSIIndicator(close=close_prices, window=period)
    return rsi.rsi()

def should_buy(market_data):
    closes = market_data.get("closes", [])
    if len(closes) < 30:
        return False
    close_series = pd.Series(closes)
    macd, signal = calculate_macd(close_series)
    rsi = calculate_rsi(close_series)
    return macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1] and rsi.iloc[-1] < 70

def should_sell(market_data, buy_price, stop_loss_percent=5, take_profit_percent=3):
    current_price = market_data.get("price", 0)
    if current_price == 0 or buy_price == 0:
        return False
    change = ((current_price - buy_price) / buy_price) * 100
    return change <= -stop_loss_percent or change >= take_profit_percent
