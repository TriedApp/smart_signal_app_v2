from TradingApp.utils.data import get_mexc_klines
from TradingApp.utils.strategy import generate_signal
from TradingApp.utils.notify import send_email, send_telegram

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

interval = "1h"

for symbol in symbols:
    print(f"\n📡 بررسی نماد: {symbol}")

    try:
        df = get_mexc_klines(symbol, interval)
        if df is None or df.empty:
            print(f"⚠️ دیتافریم خالی برای {symbol} در تایم‌فریم {interval}")
            continue
    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        continue

    df_dict = {interval: df}
    signal = generate_signal(df_dict, ai_trend="bullish", tf1h_trend="bullish")

    if signal:
        msg = (
            f"📈 سیگنال {signal['type']} برای {symbol}\n"
            f"🧠 شدت سیگنال: {signal['strength']}\n"
            f"🛑 حد ضرر: {signal['stop']}\n"
            f"🎯 حد سود: {signal['take_profit']}"
        )
        print(msg)
        send_email(msg)
        send_telegram(msg)
    else:
        print(f"⏳ هیچ سیگنالی برای {symbol} یافت نشد.")