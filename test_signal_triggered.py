from signal_dispatcher import run_strategy
import pandas as pd
import numpy as np

def generate_test_df():
    rows = 100
    df = pd.DataFrame({
        "open": np.linspace(100, 110, rows),
        "high": np.linspace(101, 111, rows),
        "low": np.linspace(99, 109, rows),
        "close": np.linspace(100.5, 110.5, rows),
        "volume": np.random.uniform(1000, 5000, rows)
    })

    # کندل قبل: قرمز و ضعیف
    df.loc[rows - 2, "open"] = 108
    df.loc[rows - 2, "close"] = 104
    df.loc[rows - 2, "low"] = 103
    df.loc[rows - 2, "high"] = 109

    # کندل فعلی: سبز، انگلفینگ، شرایط فعال‌شده
    df.loc[rows - 1, "open"] = 103
    df.loc[rows - 1, "close"] = 118  # افزایش قیمت برای تقویت MACD
    df.loc[rows - 1, "low"] = 112    # اصلاح low برای عبور از SMA10
    df.loc[rows - 1, "high"] = 119
    df.loc[rows - 1, "volume"] = 6000

    return df

if __name__ == "__main__":
    df = generate_test_df()
    signals = run_strategy(df)
    print(f"\n✅ تعداد سیگنال‌های صادر شده: {len(signals)}")
    for s in signals:
        print(f"📍 سیگنال در {s[0]} → قیمت: {s[2]:.2f} | SL: {s[3]:.2f}")