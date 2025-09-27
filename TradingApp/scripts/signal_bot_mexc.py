import os
import smtplib
import schedule
import time
from email.mime.text import MIMEText

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = os.environ['EMAIL_TO']

    # Yahoo SMTP settings
    with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

def run_bot():
    # اینجا می‌تونی سیگنال‌ها رو بررسی کنی و پیام بسازی
    msg = "✅ وضعیت ربات: هیچ سیگنالی یافت نشد."
    send_email("وضعیت ربات", msg)
    print("🚀 ربات شکار سیگنال MEXC فعال شد...")

# اجرای ربات هر 5 دقیقه
schedule.every(5).minutes.do(run_bot)

if __name__ == "__main__":
    print("🎯 ربات در حال اجراست...")
    while True:
        schedule.run_pending()
        time.sleep(1)