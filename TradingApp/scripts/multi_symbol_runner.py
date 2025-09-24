from TradingApp.generate_signal import get_mexc_data, run_strategy

def generate_all_signals():
    symbols = ["BTCUSDT", "ETHUSDT"]
    timeframe = "1h"
    all_signals = []

    for symbol in symbols:
        print(f"📡 دریافت داده برای {symbol}...")
        try:
            df = get_mexc_data(symbol, timeframe)
            signal = run_strategy(df)
            if signal:
                print(f"✅ سیگنال برای {symbol}: {signal}")
                all_signals.append({
                    "symbol": symbol,
                    "technical": signal
                })
            else:
                print(f"⏳ سیگنال برای {symbol} یافت نشد.")
        except Exception as e:
            print(f"❌ خطا در پردازش {symbol}:", e)

    return all_signals