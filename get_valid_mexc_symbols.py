import requests

# لیست نمادهای نوبیتکس
nobitex_symbols = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "TRXUSDT", "SOLUSDT", "ADAUSDT",
    "DOTUSDT", "AVAXUSDT", "SHIBUSDT", "UNIUSDT", "LINKUSDT", "MATICUSDT",
    "LTCUSDT", "BCHUSDT", "XLMUSDT", "EOSUSDT", "ATOMUSDT", "NEARUSDT",
    "FTMUSDT", "SANDUSDT", "APEUSDT", "AAVEUSDT", "GRTUSDT", "CHZUSDT",
    "ETCUSDT", "RUNEUSDT", "CRVUSDT", "1INCHUSDT", "COMPUSDT", "SNXUSDT",
    "DYDXUSDT", "ARBUSDT", "OPUSDT", "TOMOUSDT", "INJUSDT", "GMXUSDT",
    "LDOUSDT", "RNDRUSDT", "IMXUSDT", "FLOWUSDT", "CVCUSDT", "DENTUSDT"
]

# دریافت لیست نمادهای فعال از MEXC
def get_mexc_symbols():
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    try:
        response = requests.get(url)
        data = response.json()
        return [item['symbol'] for item in data['symbols']]
    except Exception as e:
        print(f"❌ خطا در دریافت لیست نمادهای MEXC: {e}")
        return []

# تطبیق با نمادهای نوبیتکس
def filter_valid_symbols():
    mexc_symbols = get_mexc_symbols()
    valid = [s for s in nobitex_symbols if s in mexc_symbols]
    print(f"✅ تعداد نمادهای معتبر: {len(valid)}")
    for symbol in valid:
        print(f"✔️ {symbol}")
    return valid

if __name__ == "__main__":
    filter_valid_symbols()