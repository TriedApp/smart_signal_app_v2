import pandas as pd
from TradingApp.utils.strategy import generate_signal
import talib

def test_stochrsi_condition():
    # داده‌هایی با نوسان برای تست همه‌ی شرط‌ها
    close_prices = [100]*20 + [95, 93, 96, 99, 104, 110, 108, 106, 109, 111]
    data = {
        "timestamp": pd.date_range(start="2023-01-01", periods=len(close_prices), freq="15min"),
        "open": [x - 1 for x in close_prices],
        "high": [x + 1 for x in close_prices],
        "low": [x - 2 for x in close_prices],
        "close": close_prices,
        "volume": [1000]*20 + [950, 970, 1100, 1200, 1300, 1400, 1350, 1320, 1380, 1450]
    }
    df = pd.DataFrame(data)
    df_dict = {"15m": df}

    # محاسبه شرط‌ها جداگانه برای دیباگ
    closes = df["close"].values
    ma10 = df["close"].rolling(window=10).mean()
    avg_volume = df["volume"].rolling(window=20).mean()

    upper, middle, lower = talib.BBANDS(df["close"], timeperiod=20)
    pb = (df["close"] - lower) / (upper - lower)
    pb_up = pb.iloc[-1] > pb.iloc[-2]

    macd, signal, _ = talib.MACD(df["close"])
    macd_up = macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]

    k, d = talib.STOCHRSI(df["close"])
    stoch_up = k.iloc[-2] < 20 and k.iloc[-1] > d.iloc[-1]

    trend_up = closes[-1] > closes[-2] > closes[-3] > closes[-4] > closes[-5]
    ma_condition_up = closes[-1] > ma10.iloc[-1]
    volume_up = df["volume"].iloc[-1] > avg_volume.iloc[-1]

    print("🔍 بررسی شرط‌های پله 6:")
    print("📌 روند کندلی:", trend_up)
    print("📌 MA10:", ma_condition_up)
    print("📌 حجم:", volume_up)
    print("📌 Bollinger برگشتی:", pb_up)
    print("📌 MACD کراس:", macd_up)
    print("📌 Stoch RSI کراس:", stoch_up)

    # بررسی تضادهای منطقی
    if trend_up and not macd_up:
        print("⚠️ تضاد: روند صعودی هست ولی MACD هنوز کراس نداده.")
    if pb_up and not volume_up:
        print("⚠️ تضاد: Bollinger برگشتی هست ولی حجم پایینه.")
    if stoch_up and not macd_up:
        print("⚠️ تضاد: Stoch RSI برگشته ولی MACD تأیید نمی‌کنه.")

    # اجرای تابع اصلی
    signal = generate_signal(df_dict)
    print("🔍 نتیجه نهایی:")
    if signal:
        print("✅ سیگنال تولید شد:", signal)
    else:
        print("❌ هیچ سیگنالی تولید نشد.")

if __name__ == "__main__":
    test_stochrsi_condition()
    print("✅ تست اجرا شد.")