from TradingApp.utils.data import get_mexc_klines
from TradingApp.utils.strategy import generate_signal
from TradingApp.utils.notify import send_email, send_telegram

symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "DOGEUSDT", "SHIBUSDT", "TRXUSDT", "ADAUSDT", "DOTUSDT", "BNBUSDT"]

for s in symbols:
    print(f"📡 دریافت داده برای {s}...")
    df = get_mexc_klines(s)
    if df.empty:
        print("⚠️ دیتافریم خالی است.")
        continue

    sig = generate_signal(df, ai="bullish", tf="bullish")
    if sig:
        msg = f"📈 سیگنال {sig['type']} برای {s}\nحد ضرر: {sig['stop']}"
        send_email(msg)
        send_telegram(msg)
    else:
        print(f"⏳ سیگنالی برای {s} یافت نشد.")