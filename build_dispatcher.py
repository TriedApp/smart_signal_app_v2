import os

dispatcher_code = '''
# -----------------------------
# signal_dispatcher.py - نسخه کامل با استراتژی پیشرفته
# -----------------------------
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

# -----------------------------
# اندیکاتورها
# -----------------------------
def sma(series, length):
    return series.rolling(length).mean()

def bollinger_bands(series, length=20, std_dev=2):
    sma_ = sma(series, length)
    std = series.rolling(length).std()
    upper = sma_ + std_dev * std
    lower = sma_ - std_dev * std
    bb_percent_b = (series - lower) / (upper - lower)
    return upper, lower, bb_percent_b

def macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def stochastic_rsi(df, length=14):
    low_min = df['low'].rolling(length).min()
    high_max = df['high'].rolling(length).max()
    return 100 * (df['close'] - low_min) / (high_max - low_min)

# -----------------------------
# کندل‌های Heikin Ashi
# -----------------------------
def heikin_ashi(df):
    ha_df = df.copy()
    ha_df['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha_open = [(df['open'][0] + df['close'][0]) / 2]
    for i in range(1, len(df)):
        ha_open.append((ha_open[i-1] + ha_df['ha_close'][i-1]) / 2)
    ha_df['ha_open'] = ha_open
    ha_df['ha_high'] = df[['high', 'low', 'open', 'close']].max(axis=1)
    ha_df['ha_low'] = df[['high', 'low', 'open', 'close']].min(axis=1)
    return ha_df

# -----------------------------
# تأیید کندل‌های Engulfing
# -----------------------------
def is_bullish_engulfing(prev, curr):
    return curr['close'] > curr['open'] and prev['close'] < prev['open'] and \
           curr['close'] > prev['open'] and curr['open'] < prev['close']

def is_bearish_engulfing(prev, curr):
    return curr['close'] < curr['open'] and prev['close'] > prev['open'] and \
           curr['close'] < prev['open'] and curr['open'] > prev['close']

# -----------------------------
# بررسی برخورد با MA برای حد سود
# -----------------------------
def check_take_profit(row, tolerance=0.001):
    for ma in ['sma10', 'sma50', 'sma200']:
        if pd.isna(row[ma]):
            continue
        if abs(row['close'] - row[ma]) / row[ma] < tolerance:
            return True
    return False

# -----------------------------
# اجرای استراتژی
# -----------------------------
def run_strategy(df):
    ha = heikin_ashi(df)
    df['ha_open'] = ha['ha_open']
    df['ha_close'] = ha['ha_close']
    df['ha_high'] = ha['ha_high']
    df['ha_low'] = ha['ha_low']

    df['sma10'] = sma(df['close'], 10)
    df['sma50'] = sma(df['close'], 50)
    df['sma200'] = sma(df['close'], 200)
    df['bb_upper'], df['bb_lower'], df['bb_percent_b'] = bollinger_bands(df['close'])
    df['macd'], df['macd_signal'], df['macd_hist'] = macd(df['close'])
    df['stoch_rsi'] = stochastic_rsi(df)

    signals = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        # --- LONG CONDITIONS ---
        long_cond = all([
            row['low'] > row['sma10'],
            prev['bb_percent_b'] < 0.2 and row['bb_percent_b'] > 0.2,
            prev['macd'] < prev['macd_signal'] and row['macd'] > row['macd_signal'],
            prev['stoch_rsi'] < 20 and row['stoch_rsi'] > 20,
            is_bullish_engulfing(prev, row),
            row['ha_close'] > row['ha_open'] and row['ha_low'] > row['ha_open'] * 0.995
        ])
        if long_cond:
            sl = row['low'] * 0.995
            tp = check_take_profit(row)
            signals.append((df.index[i], 'LONG', row['close'], sl, tp))

        # --- SHORT CONDITIONS ---
        short_cond = all([
            row['high'] < row['sma10'],
            prev['bb_percent_b'] > 0.8 and row['bb_percent_b'] < 0.8,
            prev['macd'] > prev['macd_signal'] and row['macd'] < row['macd_signal'],
            prev['stoch_rsi'] > 80 and row['stoch_rsi'] < 80,
            is_bearish_engulfing(prev, row),
            row['ha_close'] < row['ha_open'] and row['ha_high'] < row['ha_open'] * 1.005
        ])
        if short_cond:
            sl = row['high'] * 1.005
            tp = check_take_profit(row)
            signals.append((df.index[i], 'SHORT', row['close'], sl, tp))

    return signals
'''

# مسیر ذخیره‌سازی فایل dispatcher
target_path = "TradingApp/scripts/signal_dispatcher.py"
os.makedirs(os.path.dirname(target_path), exist_ok=True)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(dispatcher_code.strip())

print(f"✅ فایل dispatcher با استراتژی کامل ساخته شد و در مسیر:\n{target_path}")