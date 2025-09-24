import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TradingApp.scripts.multi_symbol_runner import generate_all_signals

import smtplib
import ssl
import requests

def format_signal(signal):
    return f"""
📡 سیگنال {signal['type']}
نماد: {signal['symbol']}
تایم‌فریم: {signal['timeframe']}
ورود: {signal['entry']}
حد ضرر: {signal['stop_loss']}
دلیل: {signal['reason']}
"""

def send_email(message):
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    if not EMAIL_USER or not EMAIL_PASS:
        print("❌ اطلاعات ایمیل ناقص است.")
        return

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_USER, message.encode("utf-8"))
            print("📤 ایمیل ارسال شد.")
    except Exception as e:
        print("❌ خطا در ارسال ایمیل:", e)

def send_telegram(message):
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ اطلاعات تلگرام ناقص است.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("📤 پیام تلگرام ارسال شد.")
        else:
            print("❌ خطا در ارسال تلگرام:", response.text)
    except Exception as e:
        print("❌ خطای تلگرام:", e)

# اجرای نهایی
signals = generate_all_signals()

if not signals:
    print("⚠️ هیچ سیگنالی تولید نشد.")
else:
    for signal in signals:
        text = format_signal(signal)
        send_email(text)
        send_telegram(text)