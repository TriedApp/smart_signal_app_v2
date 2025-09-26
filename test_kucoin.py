import subprocess
import sys
import time

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    import pandas as pd
except ImportError:
    install("pandas")
    import pandas as pd

try:
    from kucoin.client import Client
except ImportError:
    install("python-kucoin==2.1.3")
    from kucoin.client import Client

try:
    from ta.trend import EMAIndicator
    from ta.momentum import RSIIndicator
except ImportError:
    install("ta")
    from ta.trend import EMAIndicator
    from ta.momentum import RSIIndicator

client = Client('', '', '')

symbol = 'BTC-USDT'
timeframe = '1hour'
tf_ms = 3600 * 1000

now = int(time.time() * 1000)
start = now - tf_ms * 100

try:
    candles = client.get_kline_data(symbol, timeframe, start=start, end=now)

    if not candles or len(candles) < 50:
        print(f"❌ خطا: داده‌ای برای تحلیل موجود نیست یا تعداد کندل کافی نیست")
    else:
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'close', 'high', 'low', 'volume', 'turnover'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        df['EMA_20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
        df['EMA_50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
        df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()

        def generate_signal(row):
            if row['EMA_20'] > row['EMA_50'] and row['RSI'] > 50:
                return 'BUY'
            elif row['EMA_20'] < row['EMA_50'] and row['RSI'] < 50:
                return 'SELL'
            else:
                return 'HOLD'

        df['signal'] = df.apply(generate_signal, axis=1)
        latest = df.iloc[-1]

        print(f"📈 {symbol} | ⏱ {timeframe}")
        print(f"EMA20: {latest['EMA_20']:.2f}, EMA50: {latest['EMA_50']:.2f}, RSI: {latest['RSI']:.2f}")
        print(f"✅ سیگنال نهایی: {latest['signal']}")
except Exception as e:
    print(f"❌ خطا: {e}")