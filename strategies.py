import pandas as pd
import ta

def analyze(df):
    df = df.copy()
    df['ema10'] = ta.trend.ema_indicator(df['close'], window=10).ema_indicator()
    df['ema50'] = ta.trend.ema_indicator(df['close'], window=50).ema_indicator()
    df['rsi'] = ta.momentum.rsi(df['close'])
    macd = ta.trend.macd(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    latest = df.iloc[-1]
    condition = (
        latest['ema10'] > latest['ema50'] and
        latest['rsi'] < 70 and
        latest['macd'] > latest['macd_signal']
    )
    return condition