import requests
import pandas as pd
from signal_dispatcher import run_strategy

# دریافت داده کندل از MEXC
def fetch_ohlcv_mexc(symbol="BTC_USDT", interval="1h", limit=100):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    res = requests.get(url)
    data = res.json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "_", "_", "_", "_", "_", "_"
    ])
    df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df[["open", "high", "low", "close", "volume"]]

# دریافت قیمت لحظه‌ای از CoinGecko
def fetch_price_coingecko(coin_id="bitcoin", vs_currency="usd"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}&include_24hr_change=true"
    res = requests.get(url)
    data = res.json()
    price = data[coin_id][vs_currency]
    change = data[coin_id][f"{vs_currency}_24h_change"]
    return price, change

# اجرای استراتژی روی داده واقعی
if __name__ == "__main__":
    print("📡 دریافت داده از MEXC...")
    df = fetch_ohlcv_mexc("BTC_USDT", "1h", 100)

    print("🧠 اجرای استراتژی...")
    signals = run_strategy(df)

    print(f"\n✅ تعداد سیگنال‌های صادر شده: {len(signals)}")
    for s in signals:
        print(f"📍 سیگنال در {s[0]} → قیمت: {s[2]:.2f} | SL: {s[3]:.2f}")

    print("\n🌐 دریافت قیمت لحظه‌ای از CoinGecko...")
    price, change = fetch_price_coingecko("bitcoin")
    print(f"📊 قیمت بیت‌کوین: ${price:.2f} | تغییر ۲۴ ساعته: {change:.2f}%")