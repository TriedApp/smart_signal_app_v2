import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "DOGEUSDT", "SHIBUSDT", "TRXUSDT", "ADAUSDT", "DOTUSDT", "BNBUSDT",
    "SOLUSDT", "AVAXUSDT", "UNIUSDT", "LINKUSDT", "XLMUSDT", "ATOMUSDT", "EOSUSDT", "DAIUSDT", "USDCUSDT", "MATICUSDT",
    "AAVEUSDT", "AXSUSDT", "SANDUSDT", "CHZUSDT", "FTMUSDT", "NEARUSDT", "GALAUSDT", "RAYUSDT", "CAKEUSDT", "CRVUSDT",
    "1INCHUSDT", "ENJUSDT", "BCHUSDT", "ETCUSDT", "XMRUSDT", "ZECUSDT", "SNXUSDT", "COMPUSDT", "YFIUSDT", "ALGOUSDT",
    "TOMOUSDT", "KSMUSDT", "KNCUSDT", "RENUSDT", "BATUSDT", "SUSHIUSDT", "STORJUSDT", "CELRUSDT", "ANKRUSDT", "CVCUSDT",
    "BALUSDT", "GMTUSDT", "LRCUSDT", "DYDXUSDT", "GMXUSDT", "OPUSDT", "ARBUSDT", "INJUSDT", "PEPEUSDT", "FLOKIUSDT",
    "ORDIUSDT", "WLDUSDT", "TUSDUSDT", "PYTHUSDT", "BONKUSDT", "TIAUSDT", "JUPUSDT", "GRTUSDT", "RNDRUSDT", "LPTUSDT",
    "MINAUSDT", "BLURUSDT", "ICPUSDT", "APTUSDT", "SUIUSDT", "C98USDT", "XVSUSDT", "RUNEUSDT", "DODOUSDT", "HOOKUSDT",
    "SSVUSDT", "IDUSDT", "LDOUSDT", "FETUSDT", "AGIXUSDT", "OCEANUSDT", "BANDUSDT", "QNTUSDT", "STMXUSDT", "XNOUSDT",
    "NMRUSDT", "NKNUSDT", "CTSIUSDT", "SKLUSDT", "VETUSDT", "VTHOUSDT", "COTIUSDT", "MASKUSDT", "HIGHUSDT", "SPELLUSDT",
    "SXPUSDT", "DENTUSDT"
]

timeframes = {
    "5min": "300",
    "15min": "900",
    "30min": "1800",
    "1hour": "3600",
    "4hour": "14400",
    "1day": "86400"
}

def fetch_candles(symbol, period):
    url = f"https://api.coinex.com/v2/spot/kline?market={symbol}&period={period}&limit=100"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print(f"🔍 بررسی نماد: {symbol}")
            print(f"❌ API پاسخ نداد برای {symbol} | کد: {res.status_code}")
            print(f"⚠️ داده‌ای دریافت نشد.\n")
            return None
        data = res.json().get('data', [])
        if not data or len(data) < 50:
            print(f"🔍 بررسی نماد: {symbol}")
            print(f"⚠️ داده کافی نیست برای تحلیل ({len(data)} کندل)\n")
            return None
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'close', 'high', 'low', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df[['open', 'close', 'high', 'low']] = df[['open', 'close', 'high', 'low']].astype(float)
        return df
    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        return None

def analyze(df):
    df['EMA_20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
    df['EMA_50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
    df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()

    def signal(row):
        if row['EMA_20'] > row['EMA_50'] and row['RSI'] > 50:
            return 'BUY'
        elif row['EMA_20'] < row['EMA_50'] and row['RSI'] < 50:
            return 'SELL'
        else:
            return 'HOLD'

    df['signal'] = df.apply(signal, axis=1)
    return df.iloc[-1]

buy_signals = []

for symbol in symbols:
    for tf_name, tf_code in timeframes.items():
        df = fetch_candles(symbol, tf_code)
        if df is not None:
            latest = analyze(df)
            print(f"📈 {symbol} | ⏱ {tf_name}")
            print(f"EMA20: {latest['EMA_20']:.2f}, EMA50: {latest['EMA_50']:.2f}, RSI: {latest['RSI']:.2f}")
            print(f"✅ سیگنال نهایی: {latest['signal']}\n")
            if latest['signal'] == 'BUY':
                buy_signals.append((symbol, tf_name, latest['close']))

if buy_signals:
    print("🚀 سیگنال‌های BUY فعال:")
    for s in buy_signals:
        print(f"🔔 {s[0]} | ⏱ {s[1]} | قیمت: {s[2]}")
else:
    print("📉 هیچ سیگنال BUY فعالی یافت نشد.")
