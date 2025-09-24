import pandas as pd
import ta
from analysis.ml_model import predict_trend  # فرض بر اینه که مدل ML در این مسیر هست

def run_strategy(df):
    signals = []

    # محاسبات اندیکاتورها
    df['heikin_open'] = (df['open'] + df['close']) / 2
    df['heikin_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    df['ma10'] = ta.trend.sma_indicator(df['close'], window=10)
    df['macd'] = ta.trend.macd_diff(df['close'])
    df['stoch_rsi'] = ta.momentum.stochrsi_k(df['close'])
    df['volume_ma'] = ta.trend.sma_indicator(df['volume'], window=10)
    df['bollinger_b'] = ta.volatility.BollingerBands(df['close']).bollinger_pband()

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # هوش مصنوعی: پیش‌بینی روند
    trend = predict_trend(df)

    # تایم‌فریم 1h: فرض بر اینه که جداگانه بررسی شده و نتیجه‌اش به صورت ورودی میاد
    tf1h_trend = df.attrs.get("tf1h_trend", "neutral")

    # بررسی Bullish Engulfing
    bullish_engulfing = last['close'] > last['open'] and prev['close'] < prev['open'] and last['open'] < prev['close'] and last['close'] > prev['open']
    bearish_engulfing = last['close'] < last['open'] and prev['close'] > prev['open'] and last['open'] > prev['close'] and last['close'] < prev['open']

    # سیگنال خرید
    if (
        last['ma10'] < last['heikin_close'] and
        last['bollinger_b'] > 0.2 and
        last['macd'] > 0 and prev['macd'] < 0 and
        last['stoch_rsi'] > 0.2 and prev['stoch_rsi'] < 0.2 and
        bullish_engulfing and
        last['volume'] > last['volume_ma'] and
        trend == "up" and
        tf1h_trend == "up"
    ):
        stop_loss = last['low'] * 0.995
        signal = {
            "type": "LONG",
            "entry": last['close'],
            "stop_loss": round(stop_loss, 2),
            "reason": "تمام شروط خرید برقرار است"
        }
        signals.append(signal)

    # سیگنال فروش
    if (
        last['ma10'] > last['heikin_close'] and
        last['bollinger_b'] < 0.8 and
        last['macd'] < 0 and prev['macd'] > 0 and
        last['stoch_rsi'] < 0.8 and prev['stoch_rsi'] > 0.8 and
        bearish_engulfing and
        last['volume'] > last['volume_ma'] and
        trend == "down" and
        tf1h_trend == "down"
    ):
        stop_loss = last['high'] * 1.005
        signal = {
            "type": "SHORT",
            "entry": last['close'],
            "stop_loss": round(stop_loss, 2),
            "reason": "تمام شروط فروش برقرار است"
        }
        signals.append(signal)

    return signals

def get_mexc_data(symbol, interval="1h", limit=100):
    # این تابع باید دیتا رو از API بگیره و به شکل DataFrame برگردونه
    # فعلاً فرض بر اینه که آماده‌ست و فقط صدا زده می‌شه
    pass