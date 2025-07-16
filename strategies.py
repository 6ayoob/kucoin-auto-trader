import pandas as pd
import numpy as np

def calculate_macd(close_prices, short_window=12, long_window=26, signal_window=9):
    """حساب مؤشرات MACD"""
    short_ema = close_prices.ewm(span=short_window, adjust=False).mean()
    long_ema = close_prices.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def should_buy(market_data):
    """قرار الشراء باستخدام تقاطع MACD"""
    closes = market_data.get("closes", [])
    if len(closes) < 30:
        return False  # لا يوجد بيانات كافية

    close_series = pd.Series(closes)
    macd, signal = calculate_macd(close_series)

    # شرط: تقاطع MACD مع الإشارة صعودًا
    if macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]:
        return True

    return False

def should_sell(market_data, buy_price, stop_loss_percent):
    """قرار البيع بناء على Stop Loss"""
    current_price = market_data.get("price", 0)
    if current_price == 0 or buy_price == 0:
        return False

    change = ((current_price - buy_price) / buy_price) * 100
    return change <= -stop_loss_percent
