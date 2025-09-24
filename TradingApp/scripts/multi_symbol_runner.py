import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generate_signal import get_mexc_data, run_strategy

def generate_all_signals():
    # مثال ساده برای تست
    symbols = ["BTCUSDT", "ETHUSDT"]
    timeframe = "1h"
    all_signals = []

    for symbol in symbols:
        print(f"📡 دریافت داده برای {symbol}...")
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

    return all_signals