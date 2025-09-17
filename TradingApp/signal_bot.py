import requests
import smtplib
from email.mime.text import MIMEText

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
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": msg})

def send_email(msg):
    sender = "your@email.com"
    password = "your_password"
    receiver = "recipient@email.com"
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, MIMEText(msg))
    smtp.quit()

signal = get_signal()
send_telegram(signal)
send_email(signal)
print("✅ سیگنال ارسال شد:", signal)
