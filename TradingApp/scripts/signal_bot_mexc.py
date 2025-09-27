import os
import smtplib
import requests
import schedule
import time
from email.mime.text import MIMEText

SYMBOLS = [
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

API_URL = 'https://api.mexc.com/api/v3/ticker/price?symbol='

def get_prices():
    prices = {}
    for symbol in SYMBOLS:
        try:
            response = requests.get(API_URL + symbol, timeout=5)
            data = response.json()
            prices[symbol] = float(data['price'])
        except Exception as e:
            prices[symbol] = f"❌ خطا"
    return prices

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = os.environ['EMAIL_TO']

    with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

def send_telegram(text):
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def run_bot():
    prices = get_prices()
    msg_lines = ["✅ وضعیت ربات: بررسی بازار اسپات MEXC", ""]

    for symbol, price in prices.items():
        msg_lines.append(f"{symbol}: {price}")

    msg = "\n".join(msg_lines)

    send_email("📊 گزارش قیمت‌های لحظه‌ای", msg)
    send_telegram(msg)
    print("🚀 ربات شکار سیگنال MEXC فعال شد...")

schedule.every(5).minutes.do(run_bot)

if __name__ == "__main__":
    print("🎯 ربات در حال اجراست...")
    while True:
        schedule.run_pending()
        time.sleep(1)