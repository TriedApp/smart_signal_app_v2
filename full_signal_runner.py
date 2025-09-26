from signal_engine.generate_signal import get_mexc_data, run_strategy

# تحلیل تکنیکال
def get_technical_signal(symbol, timeframe):
    df = get_mexc_data(symbol=symbol, interval=timeframe)
    if df is None or df.empty:
        return {"status": "no-data"}
    
    signals = run_strategy(df)
    if not signals:
        return {"status": "no-signal"}
    
    return {
        "status": "ok",
        "action": signals[0]["action"],
        "entry": signals[0]["entry"],
        "stop_loss": signals[0]["stop_loss"],
        "take_profit": signals[0]["take_profit"]
    }

# مدل ML فرضی (داده‌محور نیست، فقط تستی)
def predict_signal(symbol, timeframe):
    # در نسخه واقعی می‌تونی از مدل‌های sklearn یا keras استفاده کنی
    # اینجا فقط یه خروجی تستی می‌دیم
    return {
        "status": "ok",
        "prediction": "buy",
        "confidence": 0.87
    }

# اجرای همزمان هر دو تحلیل
if __name__ == "__main__":
    symbol = "SHIBUSDT"
    timeframe = "1h"

    print(f"📡 دریافت سیگنال برای {symbol} | تایم‌فریم: {timeframe}\n")

    tech = get_technical_signal(symbol, timeframe)
    ml = predict_signal(symbol, timeframe)

    print("📊 تحلیل تکنیکال:")
    print(tech)

    print("\n🤖 پیش‌بینی مدل ML:")
    print(ml)