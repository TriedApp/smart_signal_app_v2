from analysis.ml_model import predict_signal  # اصلاح مسیر ایمپورت مطابق با ساختار فعلی
import pandas as pd

def get_mexc_data(symbol: str, timeframe: str) -> pd.DataFrame:
    """
    دریافت داده‌های بازار از صرافی MEXC برای نماد و تایم‌فریم مشخص‌شده.
    این تابع باید داده‌ها را از API یا فایل محلی دریافت کند.
    """
    # اینجا باید کد واقعی برای دریافت داده‌ها قرار بگیره
    # برای مثال:
    # df = fetch_from_mexc_api(symbol, timeframe)
    df = pd.DataFrame()  # جایگزین موقت
    return df

def run_strategy(df: pd.DataFrame) -> str:
    """
    اجرای مدل تحلیل تکنیکال یا یادگیری ماشین روی داده‌ها.
    خروجی باید یکی از سیگنال‌های 'buy', 'sell', یا None باشد.
    """
    if df.empty:
        print("⚠️ دیتافریم خالی است، تحلیل انجام نمی‌شود.")
        return None

    try:
        signal = predict_signal(df)
        print(f"📈 سیگنال تولید شده توسط مدل: {signal}")
        return signal
    except Exception as e:
        print("❌ خطا در اجرای مدل تحلیل:", e)
        return None