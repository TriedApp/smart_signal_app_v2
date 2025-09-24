import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TradingApp.scripts.generate_signal import get_mexc_data, run_strategy
from TradingApp.scripts.analysis.ml_model import predict_trend  # اگر مدل ML در این مسیر باشه

symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "DOGEUSDT", "BNBUSDT"
]

timeframes = ["5m", "15m", "30m", "1h"]

def generate_all_signals():
    all_signals = []

    for symbol in symbols:
        for tf in timeframes:
            print(f"🔍 بررسی {symbol} در تایم‌فریم {tf}")
            df = get_mexc_data(symbol=symbol, interval=tf, limit=100)
            if df is None or df.empty:
                print(f"⚠️ داده‌ای برای {symbol} در {tf} دریافت نشد.")
                continue

            tf1h_df = get_mexc_data(symbol=symbol, interval="1h", limit=100)
            tf1h_trend = "neutral"
            if tf1h_df is not None and not tf1h_df.empty:
                tf1h_trend = predict_trend(tf1h_df)

            df.attrs["tf1h_trend"] = tf1h_trend

            signals = run_strategy(df)
            for signal in signals:
                signal["symbol"] = symbol
                signal["timeframe"] = tf
                all_signals.append(signal)
                print("✅ سیگنال معتبر:", signal)

    print(f"\n🎯 مجموع سیگنال‌های تولیدشده: {len(all_signals)}")
    return all_signals