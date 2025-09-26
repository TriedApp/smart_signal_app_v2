import json

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

# خواندن فایل exchange_info.json
with open("exchange_info.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# استخراج نمادهای فعال
mexc_symbols = [
    item["symbol"] for item in data.get("symbols", [])
    if item.get("isSpotTradingAllowed") and item.get("status") == "1"
]

# تطبیق با نمادهای نوبیتکس
valid = [s for s in nobitex_symbols if s in mexc_symbols]

# ذخیره در config.py
with open("config.py", "w", encoding="utf-8") as f:
    f.write("valid_symbols = [\n")
    for symbol in valid:
        f.write(f'    "{symbol}",\n')
    f.write("]\n")

print(f"✅ لیست نمادهای معتبر ذخیره شد ({len(valid)} نماد):")
for s in valid:
    print(f"✔️ {s}")