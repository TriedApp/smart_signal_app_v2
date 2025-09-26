import pandas as pd
import numpy as np
from signal_dispatcher import run_strategy

def generate_triggered_df():
    rows = 100
    df = pd.DataFrame({
        "open": np.linspace(100, 110, rows),
        "high": np.linspace(101, 111, rows),
        "low": np.linspace(99, 109, rows),
        "close": np.linspace(100.5, 110.5, rows),
        "volume": np.random.uniform(1000, 5000, rows)
    })

    # اعمال شرایط مصنوعی برای فعال شدن سیگنال در انتهای دیتافریم
    df.iloc[-2]["close"] = 98  # کندل قرمز قبلی
    df.iloc[-2]["open"] = 100

    df.iloc[-1]["close"] = 102  # کندل سبز فعلی
    df.iloc[-1]["open"] = 99

    df.iloc[-1]["low"] = 98.5
    df.iloc[-1]["high"] = 103

    return df

if __name__ == "__main__":
    df = generate_triggered_df()
    signals = run_strategy(df)
    print(f"✅ تعداد سیگنال‌های صادر شده: {len(signals)}")
    for s in signals:
        print(f"📍 سیگنال در {s[0]} → قیمت: {s[2]:.2f} | SL: {s[3]:.2f} | TP: {'✅' if s[4] else '❌'}")