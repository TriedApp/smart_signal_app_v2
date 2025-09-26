from TradingApp.utils.data import get_mexc_klines
from TradingApp.utils.strategy import generate_signal
from TradingApp.utils.notify import send_email, send_telegram

# نمادها با فرمت صحیح برای MEXC
symbols = [
    "BTC_USDT", "ETH_USDT", "XRP_USDT", "LTC_USDT", "DOGE_USDT",
    "SHIB_USDT", "TRX_USDT", "ADA_USDT", "DOT_USDT", "BNB_USDT"
]

# فقط تایم‌فریم 1h برای تحلیل فعلی
interval = "1h"

for symbol in symbols:
    print(f"\n📡 بررسی نماد: {symbol}")

    try:
        df = get_mexc_klines(symbol, interval)
        if df is None or df.empty:
            print(f"⚠️ دیتافریم خالی برای {symbol} در تایم‌فریم {interval}")
            continue
    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        continue

    # ساخت دیکشنری تایم‌فریم برای استراتژی
    df_dict = {interval: df}

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