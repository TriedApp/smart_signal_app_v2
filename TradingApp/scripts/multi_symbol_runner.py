from TradingApp.generate_signal import get_binance_data, run_strategy
import pandas as pd

def generate_all_signals(symbols: list, interval: str = "1h") -> dict:
    """
    دریافت داده برای چند نماد و اجرای استراتژی تحلیل روی هر کدام.
    خروجی: دیکشنری از سیگنال‌ها
    """
    signals = {}

    for symbol in symbols:
        print(f"📡 دریافت داده برای {symbol}...")
        df = get_binance_data(symbol, interval)
        signal = run_strategy(df)

        if signal:
            print(f"✅ سیگنال برای {symbol}: {signal}")
            signals[symbol] = signal
        else:
            print(f"⏳ سیگنال برای {symbol} یافت نشد.")
            signals[symbol] = None

    return signals