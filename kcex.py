import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

symbols = ["BTC_USDT", "ETH_USDT", "SOL_USDT", "XRP_USDT", "DOGE_USDT"]
timeframes = {
    "5min": "5m",
    "15min": "15m",
    "1hour": "1h",
    "4hour": "4h",
    "1day": "1d"
}

def fetch_kline(symbol, interval):
    url = f"https://api.kcex.com/api/v1/market/kline?symbol={symbol}&interval={interval}&limit=100"
    try:
        res = requests.get(url, timeout=10)
        data = res.json().get("data", [])
        if not data or len(data) < 50:
            print(f"⚠️ داده کافی نیست برای {symbol} | تایم‌فریم: {interval}")
            return None
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
        return df
    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        return None

def analyze(df):
    df["EMA20"] = EMAIndicator(close=df["close"], window=20).ema_indicator()
    df["EMA50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()
    df["RSI"] = RSIIndicator(close=df["close"], window=14).rsi()

    def signal(row):
        if row["EMA20"] > row["EMA50"] and row["RSI"] > 50:
            return "BUY"
        elif row["EMA20"] < row["EMA50"] and row["RSI"] < 50:
            return "SELL"
        else:
            return "HOLD"

    df["signal"] = df.apply(signal, axis=1)
    return df.iloc[-1]

buy_signals = []

for symbol in symbols:
    for tf_name, tf_code in timeframes.items():
        df = fetch_kline(symbol, tf_code)
        if df is not None:
            latest = analyze(df)
            print(f"📊 {symbol} | ⏱ {tf_name}")
            print(f"EMA20: {latest['EMA20']:.2f}, EMA50: {latest['EMA50']:.2f}, RSI: {latest['RSI']:.2f}")
            print(f"✅ سیگنال نهایی: {latest['signal']}\n")
            if latest["signal"] == "BUY":
                buy_signals.append((symbol, tf_name, latest["close"]))

if buy_signals:
    print("🚀 سیگنال‌های BUY فعال:")
    for s in buy_signals:
        print(f"🔔 {s[0]} | ⏱ {s[1]} | قیمت: {s[2]}")
else:
    print("📉 هیچ سیگنال BUY فعالی یافت نشد.")