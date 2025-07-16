import pandas as pd
import ta

def should_buy(closes):
    df = pd.DataFrame(closes, columns=["close"])
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    return df["rsi"].iloc[-1] < 30 and df["macd"].iloc[-1] > df["macd_signal"].iloc[-1]

def should_sell(closes):
    df = pd.DataFrame(closes, columns=["close"])
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    return df["rsi"].iloc[-1] > 70 and df["macd"].iloc[-1] < df["macd_signal"].iloc[-1]
