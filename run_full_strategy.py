import requests
import pandas as pd
from signal_dispatcher import run_strategy

valid_symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "DOGEUSDT", "SHIBUSDT",
    "TRXUSDT", "ADAUSDT", "DOTUSDT", "BNBUSDT", "SOLUSDT", "AVAXUSDT",
    "UNIUSDT", "LINKUSDT", "XLMUSDT", "ATOMUSDT", "EOSUSDT", "DAIUSDT",
    "USDCUSDT", "MATICUSDT", "AAVEUSDT", "AXSUSDT", "SANDUSDT", "CHZUSDT",
    "FTMUSDT", "NEARUSDT", "GALAUSDT", "RAYUSDT", "CAKEUSDT", "CRVUSDT",
    "1INCHUSDT", "ENJUSDT", "BCHUSDT", "ETCUSDT", "XMRUSDT", "ZECUSDT",
    "SNXUSDT", "COMPUSDT", "YFIUSDT", "ALGOUSDT", "TOMOUSDT", "KSMUSDT",
    "KNCUSDT", "RENUSDT", "BATUSDT", "SUSHIUSDT", "STORJUSDT", "CELRUSDT",
    "ANKRUSDT", "CVCUSDT", "BALUSDT", "GMTUSDT", "LRCUSDT", "DYDXUSDT",
    "GMXUSDT", "OPUSDT", "ARBUSDT", "INJUSDT", "PEPEUSDT", "FLOKIUSDT",
    "ORDIUSDT", "WLDUSDT", "TUSDUSDT", "PYTHUSDT", "BONKUSDT", "TIAUSDT",
    "JUPUSDT", "GRTUSDT", "RNDRUSDT", "LPTUSDT", "MINAUSDT", "BLURUSDT",
    "ICPUSDT", "APTUSDT", "SUIUSDT", "C98USDT", "XVSUSDT", "RUNEUSDT",
    "DODOUSDT", "HOOKUSDT", "SSVUSDT", "IDUSDT", "LDOUSDT", "FETUSDT",
    "AGIXUSDT", "OCEANUSDT", "BANDUSDT", "QNTUSDT", "STMXUSDT", "XNOUSDT",
    "NMRUSDT", "NKNUSDT", "CTSIUSDT", "SKLUSDT", "VETUSDT", "VTHOUSDT",
    "COTIUSDT", "MASKUSDT", "HIGHUSDT", "SPELLUSDT", "SXPUSDT", "DENTUSDT"
]

def fetch_ohlcv_mexc(symbol, interval="1h", limit=100):
    symbol_mexc = symbol.replace("USDT", "_USDT")
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol_mexc}&interval={interval}&limit={limit}"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print(f"❌ API پاسخ نداد برای {symbol} | کد: {res.status_code}")
            return pd.DataFrame()
        data = res.json()
        if not isinstance(data, list) or len(data) == 0:
            print(f"⚠️ پاسخ API خالی یا نامعتبر برای {symbol}")
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "_", "_", "_", "_", "_", "_"
        ])
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df[["open", "high", "low", "close", "volume"]]
    except Exception as e:
        print(f"⚠️ خطا در دریافت داده برای {symbol}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    total_signals = 0
    print("🚀 اجرای استراتژی روی نمادهای MEXC...\n")

    for symbol in valid_symbols:
        print(f"🔍 بررسی نماد: {symbol}")
        df = fetch_ohlcv_mexc(symbol)
        if df.empty:
            print("⚠️ داده‌ای دریافت نشد.\n")
            continue

        signals = run_strategy(df)
        if signals:
            total_signals += len(signals)
            for s in signals:
                print(f"📍 سیگنال در {symbol} → زمان: {s[0]} | قیمت: {s[2]:.2f} | SL: {s[3]:.2f}")
        else:
            print("❌ سیگنالی صادر نشد.")
        print("-" * 50)

    print(f"\n✅ مجموع سیگنال‌های صادر شده: {total_signals}")