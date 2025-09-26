from TradingApp.utils.data import get_mexc_klines
from TradingApp.utils.strategy import generate_signal
from TradingApp.utils.notify import send_email, send_telegram

symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "DOGEUSDT", "SHIBUSDT", "TRXUSDT", "ADAUSDT", "DOTUSDT", "BNBUSDT"
]

# تایم‌فریم‌های معتبر برای MEXC
intervals = ["5m", "15m", "30m", "1h", "4h", "1d"]

for symbol in symbols:
    print(f"\n📡 بررسی نماد: {symbol}")
    df_dict = {}

    for interval in intervals:
        try:
            df = get_mexc_klines(symbol, interval)
            if df is not None and not df.empty:
                df_dict[interval] = df
            else:
                print(f"⚠️ دیتافریم خالی برای {symbol} در تایم‌فریم {interval}")
        except Exception as e:
            print(f"❌ خطا در دریافت داده {interval} برای {symbol}: {e}")

    # بررسی سیگنال فقط اگر داده تایم‌فریم 1h موجود باشه
    if "1h" not in df_dict or df_dict["1h"].empty:
        print(f"⚠️ داده تایم‌فریم 1h برای {symbol} موجود نیست، تحلیل انجام نمی‌شود.")
        continue

    signal = generate_signal(df_dict, ai_trend="bullish", tf1h_trend="bullish")

    if signal:
        msg = (
            f"📈 سیگنال {signal['type']} برای {symbol}\n"
            f"🧠 شدت سیگنال: {signal['strength']}\n"
            f"🛑 حد ضرر: {signal['stop']}\n"
            f"🎯 حد سود: {signal['take_profit']}"
        )
        print(msg)
        send_email(msg)
        send_telegram(msg)
    else:
        print(f"⏳ هیچ سیگنالی برای {symbol} یافت نشد.")