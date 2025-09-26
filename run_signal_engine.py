from signal_engine.generate_signal import get_mexc_data, run_strategy

symbol = "SHIBUSDT"
interval = "1h"

print(f"📡 دریافت داده از MEXC برای {symbol} | تایم‌فریم: {interval}")
df = get_mexc_data(symbol=symbol, interval=interval)

if df is None or df.empty:
    print("❌ دریافت داده ناموفق یا خالی بود.")
else:
    print("✅ داده دریافت شد. اجرای استراتژی...")
    signals = run_strategy(df)

    if signals:
        print("🚀 سیگنال‌های فعال:")
        for s in signals:
            print(f"🔔 {s['action']} | نماد: {s['symbol']} | قیمت ورود: {s['entry']:.4f} | SL: {s['stop_loss']:.4f} | TP: {'✅' if s['take_profit'] else '❌'}")
    else:
        print("📉 هیچ سیگنال فعالی یافت نشد.")