import pandas as pd
import numpy as np
from signal_dispatcher import run_strategy

def generate_confirmed_df():
    rows = 100
    df = pd.DataFrame({
        "open": np.linspace(100, 110, rows),
        "high": np.linspace(101, 111, rows),
        "low": np.linspace(99, 109, rows),
        "close": np.linspace(100.5, 110.5, rows),
        "volume": np.random.uniform(1000, 5000, rows)
    })

    # فعال‌سازی بولیش انگلفینگ
    df.loc[rows - 2, "open"] = 105
    df.loc[rows - 2, "close"] = 102  # کندل قرمز قبلی

    df.loc[rows - 1, "open"] = 101
    df.loc[rows - 1, "close"] = 106  # کندل سبز فعلی و بولیش انگلفینگ
    df.loc[rows - 1, "low"] = 100.5
    df.loc[rows - 1, "high"] = 107

    # فعال‌سازی Bollinger Percent B
    df.loc[rows - 2, "close"] = 100  # زیر باند پایین
    df.loc[rows - 1, "close"] = 106  # عبور از باند پایین

    # فعال‌سازی MACD کراس مثبت
    df.loc[rows - 2, "close"] = 100
    df.loc[rows - 1, "close"] = 106

    # فعال‌سازی Stoch RSI عبور از 20
    df.loc[rows - 2, "low"] = 95
    df.loc[rows - 2, "high"] = 100
    df.loc[rows - 2, "close"] = 96

    df.loc[rows - 1, "low"] = 100
    df.loc[rows - 1, "high"] = 107
    df.loc[rows - 1, "close"] = 106

    # فعال‌سازی شرط SMA10
    df.loc[rows - 1, "low"] = 108  # بالاتر از میانگین

    return df

if __name__ == "__main__":
    df = generate_confirmed_df()
    signals = run_strategy(df)
    print(f"✅ تعداد سیگنال‌های صادر شده: {len(signals)}")
    for s in signals:
        print(f"📍 سیگنال در {s[0]} → قیمت: {s[2]:.2f} | SL: {s[3]:.2f} | TP: {'✅' if s[4] else '❌'}")