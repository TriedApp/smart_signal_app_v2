from dotenv import load_dotenv
import os
import requests
import smtplib
from email.mime.text import MIMEText

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

def get_signal():
    try:
        r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=10)
        price = r.json()["bpi"]["USD"]["rate_float"]
        if price > 30000:
            return f"📈 قیمت بیت‌کوین بالاست: ${price}"
        else:
            return f"📉 قیمت بیت‌کوین پایین‌تره: ${price}"
    except Exception as e:
        return f"❌ خطا در دریافت سیگنال: {e}"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

def send_email(msg):
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(EMAIL_USER, EMAIL_PASS)
    smtp.sendmail(EMAIL_USER, EMAIL_TO, MIMEText(msg))
    smtp.quit()

signal = get_signal()
send_telegram(signal)
send_email(signal)
print("✅ سیگنال ارسال شد:", signal)
