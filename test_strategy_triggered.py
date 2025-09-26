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

    # فعال‌سازی تمام شروط در کندل آخر
    i = df.index[-1]
    df.loc[i - 1, "open"] = 105
    df.loc[i - 1, "close"] = 102  # کندل قرمز قبلی

    df.loc[i, "open"] = 101
    df.loc[i, "close"] = 106  # کندل سبز فعلی و بولیش انگلفینگ
    df.loc[i, "low"] = 100.5
    df.loc[i, "high"] = 107

    # تقویت شرایط Bollinger و MACD و Stoch RSI
    df.loc[i - 1, "close"] = 100  # پایین‌تر از باند پایین
    df.loc[i, "close"] = 106     # عبور از باند پایین

    # افزایش حجم برای اعتبار بیشتر
    df.loc[i, "volume"] = 6000

    return df

if __name__ == "__main__":
    df = generate_triggered_df()
    signals = run_strategy(df)
    print(f"✅ تعداد سیگنال‌های صادر شده: {len(signals)}")
    for s in signals:
        print(f"📍 سیگنال در {s[0]} → قیمت: {s[2]:.2f} | SL: {s[3]:.2f} | TP: {'✅' if s[4] else '❌'}")