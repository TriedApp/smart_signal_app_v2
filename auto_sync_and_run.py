import requests
import subprocess

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

# ذخیره لیست معتبر در config.py
def save_valid_symbols(valid):
    with open("config.py", "w", encoding="utf-8") as f:
        f.write("valid_symbols = [\n")
        for symbol in valid:
            f.write(f'    "{symbol}",\n')
        f.write("]\n")
    print(f"✅ لیست نمادهای معتبر در config.py ذخیره شد ({len(valid)} نماد)")

# اجرای فایل signal_dispatcher.py
def run_dispatcher():
    print("🚀 اجرای فایل signal_dispatcher.py با نمادهای معتبر...")
    subprocess.run(["python", "signal_dispatcher.py"])

# اجرای کامل
if __name__ == "__main__":
    mexc_symbols = get_mexc_symbols()
    valid = [s for s in nobitex_symbols if s in mexc_symbols]
    save_valid_symbols(valid)
    run_dispatcher()