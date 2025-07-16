import ta
import pandas as pd

def apply_strategy(df):
    df['EMA20'] = ta.trend.ema_indicator(df['close'], window=20).ema_indicator()
    df['MACD'] = ta.trend.macd_diff(df['close'])
    df['RSI'] = ta.momentum.RSIIndicator(df['close']).rsi()

    latest = df.iloc[-1]
    if latest['close'] > latest['EMA20'] and latest['MACD'] > 0 and latest['RSI'] < 70:
        return "buy"
    elif latest['MACD'] < 0 and latest['RSI'] > 50:
        return "sell"
    return "hold"
