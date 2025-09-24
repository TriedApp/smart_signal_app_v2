from TradingApp.generate_signal import get_binance_data, run_strategy
import pandas as pd

def generate_all_signals(symbols: list, interval: str = "1h") -> list:
    """
    دریافت داده برای چند نماد و اجرای استراتژی تحلیل روی هر کدام.
    خروجی: لیستی از سیگنال‌ها با ساختار دیکشنری
    """
    signals = []

    for symbol in symbols:
        print(f"📡 دریافت داده برای {symbol}...")
        df = get_binance_data(symbol, interval)
        signal_type = run_strategy(df)

        if signal_type:
            print(f"✅ سیگنال برای {symbol}: {signal_type}")
            signals.append({
                "symbol": symbol,
                "technical": signal_type,
                "entry": 0.00000000,       # قابل تنظیم در آینده
                "stop_loss": 0.00000000,   # قابل تنظیم در آینده
                "take_profit": None        # قابل محاسبه در آینده
            })
        else:
            print(f"⏳ سیگنالی برای {symbol} یافت نشد.")

    return signals