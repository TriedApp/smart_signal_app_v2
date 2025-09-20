import requests
import pandas as pd
import numpy as np

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
    stoch = 100 * (df['close'] - low_min) / (high_max - low_min)
    return stoch

def is_bullish_engulfing(prev, curr):
    return curr['close'] > curr['open'] and prev['close'] < prev['open'] and            curr['close'] > prev['open'] and curr['open'] < prev['close']

def is_bearish_engulfing(prev, curr):
    return curr['close'] < curr['open'] and prev['close'] > prev['open'] and            curr['close'] < prev['open'] and curr['open'] > prev['close']

def get_mexc_data(symbol='SHIB_USDT', interval='1h', limit=100):
    url = f"https://api.mexc.com/api/v3/klines"
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    r = requests.get(url, params=params)
    data = r.json()
    df = pd.DataFrame(data, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'trades', 'taker_base_vol',
        'taker_quote_vol', 'ignore'
    ])
    df['time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('time', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

def check_take_profit(row, tolerance=0.001):
    for ma in ['sma10', 'sma50', 'sma200']:
        if pd.isna(row[ma]):
            continue
        if abs(row['close'] - row[ma]) / row[ma] < tolerance:
            return True
    return False

def run_strategy(df):
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
            is_bullish_engulfing(prev, row)
        ])
        if long_cond:
            sl = row['low'] * 0.995
            tp = check_take_profit(row)
            signals.append({
                "symbol": "SHIBUSDT",
                "action": "BUY",
                "entry": row['close'],
                "stop_loss": sl,
                "take_profit": tp
            })

        short_cond = all([
            row['high'] < row['sma10'],
            prev['bb_percent_b'] > 0.8 and row['bb_percent_b'] < 0.8,
            prev['macd'] > prev['macd_signal'] and row['macd'] < row['macd_signal'],
            prev['stoch_rsi'] > 80 and row['stoch_rsi'] < 80,
            is_bearish_engulfing(prev, row)
        ])
        if short_cond:
            sl = row['high'] * 1.005
            tp = check_take_profit(row)
            signals.append({
                "symbol": "SHIBUSDT",
                "action": "SELL",
                "entry": row['close'],
                "stop_loss": sl,
                "take_profit": tp
            })

    return signals
