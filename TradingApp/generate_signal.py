from analysis.ml_model import predict_signal  # ایمپورت مدل تحلیل
import pandas as pd
import requests

def get_binance_data(symbol: str, interval: str = "1h", limit: int = 100) -> pd.DataFrame:
    """
    دریافت داده‌های کندل از Binance بدون نیاز به API Key.
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ خطا در دریافت داده از Binance برای {symbol}: {e}")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades", "taker_buy_volume",
        "taker_buy_quote", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def run_strategy(df: pd.DataFrame) -> str:
    """
    اجرای مدل تحلیل روی داده‌های بازار.
    خروجی: 'buy', 'sell', یا None
    """
    if df.empty:
        print("⚠️ دیتافریم خالی است، تحلیل انجام نمی‌شود.")
        return None

    try:
        signal = predict_signal(df)
        print(f"📈 سیگنال تولید شده توسط مدل: {signal}")
        return signal
    except Exception as e:
        print("❌ خطا در اجرای مدل تحلیل:", e)
        return None