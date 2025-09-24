import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from TradingApp.scripts.generate_signal import get_mexc_data, run_strategy

# لیست نمادها
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

# لیست تایم‌فریم‌ها
timeframes = ["5m", "15m", "30m", "1h", "4h", "1d"]

def format_signal(signal):
    return (
        f"📡 سیگنال جدید:\n"
        f"نماد: {signal['symbol']}\n"
        f"تایم‌فریم: {signal['timeframe']}\n"
        f"عملیات: {signal['action']}\n"
        f"ورود: {signal['entry']:.8f}\n"
        f"حد ضرر: {signal['stop_loss']:.8f}\n"
        f"{'✅ حد سود فعال' if signal['take_profit'] else '⏳ در انتظار حد سود'}"
    )

def send_email(signal_text):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO") or email_user
    if not email_user or not email_pass:
        print("❌ ایمیل تنظیم نشده.")
        return
    try:
        smtp = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
        smtp.login(email_user, email_pass)
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_to
        msg["Subject"] = "📈 سیگنال معاملاتی جدید"
        msg.attach(MIMEText(signal_text, "plain"))
        smtp.send_message(msg)
        smtp.quit()
        print("✅ ایمیل ارسال شد.")
    except Exception as e:
        print("❌ خطا در ارسال ایمیل:", e)

def send_telegram(signal_text):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("❌ تلگرام تنظیم نشده.")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": signal_text}
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print("✅ پیام تلگرام ارسال شد.")
        else:
            print("❌ خطا در ارسال تلگرام:", r.text)
    except Exception as e:
        print("❌ خطای تلگرام:", e)

if __name__ == "__main__":
    print("🚀 شروع اجرای فایل signal_bot.py")
    total_signals = 0
    for symbol in symbols:
        for tf in timeframes:
            print(f"🔍 بررسی {symbol} در تایم‌فریم {tf}")
            df = get_mexc_data(symbol=symbol, interval=tf, limit=100)
            if df is None or df.empty:
                continue
            signals = run_strategy(df)
            for signal in signals:
                signal["symbol"] = symbol
                signal["timeframe"] = tf
                signal_text = format_signal(signal)
                print("✅ سیگنال:", signal_text)
                send_email(signal_text)
                send_telegram(signal_text)
                total_signals += 1
    print(f"🏁 پایان اجرا | مجموع سیگنال‌ها: {total_signals}")