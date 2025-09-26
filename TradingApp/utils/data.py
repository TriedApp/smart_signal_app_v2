import requests
import pandas as pd

def get_mexc_klines(symbol, interval, market="spot", limit=100):
    if market == "futures":
        url = f"https://contract.mexc.com/api/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    else:
        url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # برای فیوچرز، داده‌ها در key 'data' هستن
        if market == "futures":
            data = data.get("data", [])

        df = pd.DataFrame(data)
        if market == "futures":
            df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
        else:
            df.columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore"]
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.astype(float, errors="ignore")
        return df

    except Exception as e:
        print(f"❌ خطا در دریافت داده از MEXC برای {symbol}: {e}")
        return pd.DataFrame()