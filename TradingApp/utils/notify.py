import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

def send_email(body: str):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO") or email_user

    if not email_user or not email_pass:
        print("❌ متغیرهای ایمیل تعریف نشده‌اند.")
        return

    try:
        smtp = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
        smtp.login(email_user, email_pass)

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_to
        msg["Subject"] = "📈 سیگنال معاملاتی جدید"
        msg.attach(MIMEText(body, "plain"))

        smtp.send_message(msg)
        smtp.quit()
        print("✅ ایمیل ارسال شد.")
    except Exception as e:
        print("❌ خطا در ارسال ایمیل:", e)

def send_telegram(text: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("❌ متغیرهای تلگرام تعریف نشده‌اند.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print("✅ پیام تلگرام ارسال شد.")
        else:
            print("❌ خطا در ارسال تلگرام:", r.text)
    except Exception as e:
        print("❌ خطای عمومی تلگرام:", e)