import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ فایل ساخته شد: {path}")

# -----------------------------
# فایل signal_engine/generate_signal.py
# -----------------------------
generate_signal_code = '''\
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
    return curr['close'] > curr['open'] and prev['close'] < prev['open'] and \
           curr['close'] > prev['open'] and curr['open'] < prev['close']

def is_bearish_engulfing(prev, curr):
    return curr['close'] < curr['open'] and prev['close'] > prev['open'] and \
           curr['close'] < prev['open'] and curr['open'] > prev['close']

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
'''

# -----------------------------
# فایل scripts/signal_bot.py
# -----------------------------
signal_bot_code = '''\
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from signal_engine.generate_signal import get_mexc_data, run_strategy

def format_signal(signal):
    return (
        f"📡 سیگنال جدید:\\n"
        f"نماد: {signal['symbol']}\\n"
        f"عملیات: {signal['action']}\\n"
        f"ورود: {signal['entry']:.8f}\\n"
        f"حد ضرر: {signal['stop_loss']:.8f}\\n"
        f"{'✅ حد سود فعال' if signal['take_profit'] else '⏳ در انتظار حد سود'}"
    )

def send_email(signal_text):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(email_user, email_pass)

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_user
        msg["Subject"] = "📈 سیگنال معاملاتی جدید"
        msg.attach(MIMEText(signal_text, "plain"))

        smtp.send_message(msg)
        smtp.quit()
        print("✅ سیگنال با موفقیت ارسال شد.")

    except smtplib.SMTPAuthenticationError as e:
        print("❌ خطای احراز هویت SMTP:", e)
    except Exception as e:
        print("❌ خطای عمومی:", e)

if __name__ == "__main__":
    df = get_mexc_data()
    signals = run_strategy(df)
    for signal in signals:
        signal_text = format_signal(signal)
        send_email(signal_text)
'''

# -----------------------------
# فایل .github/workflows/test-smtp.yml
# -----------------------------
workflow_code = '''\
name: Signal Dispatcher

on:
  workflow_dispatch:

jobs:
  send-signal:
    runs-on: ubuntu-latest
    env:
      EMAIL_USER: ${{ secrets.EMAIL_USER }}
      EMAIL_PASS: ${{ secrets.EMAIL_PASS }}

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pandas numpy requests

      - name: Run signal dispatcher
        run: python TradingApp/scripts/signal_bot.py
'''

# -----------------------------
# اجرای ساخت فایل‌ها
# -----------------------------
write_file("TradingApp/signal_engine/generate_signal.py", generate_signal_code)
write_file("TradingApp/scripts/signal_bot.py", signal_bot_code)
write_file("TradingApp/.github/workflows/test-smtp.yml", workflow_code)

print("🎯 پروژه سیگنال‌دهی با موفقیت ساخته شد.")