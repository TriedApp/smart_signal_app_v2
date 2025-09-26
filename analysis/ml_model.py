import pandas as pd

def predict_signal(df: pd.DataFrame) -> str:
    """
    تحلیل ساده بر اساس تغییرات قیمت در آخرین کندل‌ها.
    اگر میانگین تغییرات مثبت باشد → سیگنال خرید
    اگر منفی باشد → سیگنال فروش
    """
    if df.empty or 'close' not in df.columns:
        return None

    recent = df['close'].tail(5)
    avg_change = recent.pct_change().mean()

    if avg_change > 0.01:
        return 'buy'
    elif avg_change < -0.01:
        return 'sell'
    else:
        return None

def predict_trend(df: pd.DataFrame) -> str:
    """
    تحلیل روند کلی بازار با میانگین متحرک.
    اگر MA20 > MA50 → روند صعودی
    اگر MA20 < MA50 → روند نزولی
    """
    if df.empty or 'close' not in df.columns:
        return None

    ma_20 = df['close'].rolling(window=20).mean().iloc[-1]
    ma_50 = df['close'].rolling(window=50).mean().iloc[-1]

    if ma_20 > ma_50:
        return 'uptrend'
    elif ma_20 < ma_50:
        return 'downtrend'
    else:
        return 'sideways'