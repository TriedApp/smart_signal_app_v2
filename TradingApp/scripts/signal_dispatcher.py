import requests
import pandas as pd
import numpy as np

# لیست نمادهای نوبیتکس با فیلتر نمادهای ناقص
excluded = [
    "IMXUSDT", "FLOWUSDT", "CVCUSDT", "DENTUSDT",
    "TOMOUSDT", "INJUSDT", "GMXUSDT", "LDOUSDT", "RNDRUSDT",
    "DYDXUSDT", "ARBUSDT", "OPUSDT"
]
nobitex_symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "TRXUSDT", "SOLUSDT", "ADAUSDT",
    "DOTUSDT", "AVAXUSDT", "SHIBUSDT", "UNIUSDT", "LINKUSDT", "MATICUSDT",
    "LTCUSDT", "BCHUSDT", "XLMUSDT", "EOSUSDT", "ATOMUSDT", "NEARUSDT",
    "FTMUSDT", "SANDUSDT", "APEUSDT", "AAVEUSDT", "GRTUSDT", "CHZUSDT",
    "ETCUSDT", "RUNEUSDT", "CRVUSDT", "1INCHUSDT", "COMPUSDT", "SNXUSDT"
]
valid_symbols = [s for s in nobitex_symbols if s not in excluded]

# دریافت داده از MEXC
def fetch_ohlcv_mexc(symbol, interval="15m", limit=300):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        if not isinstance(data, list) or len(data) == 0 or len(data[0]) < 6:
            print(f"⚠️ داده ناقص برای {symbol}")
            return None
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume"
        ])
        df = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df
    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        return None

# اندیکاتورها و استراتژی
def sma(series, length): return series.rolling(length).mean()

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

def is_bullish_engulfing(prev, curr):
    return curr['close'] > curr['open'] and prev['close'] < prev['open'] and \
           curr['close'] > prev['open'] and curr['open'] < prev['close']

def check_take_profit(row, tolerance=0.001):
    for ma in ['sma10', 'sma50', 'sma200']:
        if pd.isna(row[ma]): continue
        if abs(row['close'] - row[ma]) / row[ma] < tolerance:
            return True
    return False

# اجرای استراتژی با بررسی شروط
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

    # بررسی دقیق کندل آخر
    row = df.iloc[-1]
    prev = df.iloc[-2]
    print("\n🔍 بررسی کندل آخر:")
    print(f"SMA10: {row['sma10']:.2f}, Low: {row['low']:.2f}")
    print(f"BB% Prev: {prev['bb_percent_b']:.2f}, BB% Now: {row['bb_percent_b']:.2f}")
    print(f"MACD Prev: {prev['macd']:.2f}, Signal Prev: {prev['macd_signal']:.2f}")
    print(f"MACD Now: {row['macd']:.2f}, Signal Now: {row['macd_signal']:.2f}")
    print(f"Stoch RSI Prev: {prev['stoch_rsi']:.2f}, Now: {row['stoch_rsi']:.2f}")
    print(f"HA Open: {row['ha_open']:.2f}, HA Close: {row['ha_close']:.2f}, HA Low: {row['ha_low']:.2f}")
    print(f"Engulfing: {is_bullish_engulfing(prev, row)}")

    return signals

# اجرای بررسی همه نمادها
def run_all():
    print("🚀 شروع بررسی نمادهای نوبیتکس...")
    for symbol in valid_symbols:
        df = fetch_ohlcv_mexc(symbol)
        if df is None or len(df) < 50:
            print(f"⚠️ داده کافی برای {symbol} موجود نیست.")
            continue
        signals = run_strategy(df)
        if not signals:
            print(f"❌ هیچ سیگنالی برای {symbol} صادر نشد.")
        for s in signals:
            print(f"✅ سیگنال برای {symbol} در {s[0]} → قیمت: {s[2]:.2f}