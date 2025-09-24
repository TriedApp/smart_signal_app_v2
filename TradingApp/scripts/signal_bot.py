from TradingApp.scripts.multi_symbol_runner import generate_all_signals
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

def format_signal(signal):
    return (
        f"📡 سیگنال جدید:\n"
        f"نماد: {signal['symbol']}\n"
        f"عملیات: {signal['technical']}\n"
        f"ورود: 0.00000000\n"
        f"حد ضرر: 0.00000000\n"
        f"{'✅ حد سود فعال' if signal['technical'] == 'buy' else '⏳ در انتظار حد سود'}"
    )

def send_email(signal_text):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO") or email_user

    print("📤 ایمیل فرستنده:", email_user)
    print("📤 ایمیل گیرنده:", email_to)

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
        print("❌ متغیرهای تلگرام تعریف نشده‌اند.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": signal_text}

    try:
        r = requests.post(url, json=payload)
        print(f"📡 پاسخ تلگرام: {r.status_code} | {r.text[:100]}")
        if r.status_code == 200:
            print("✅ پیام تلگرام ارسال شد.")
        else:
            print("❌ خطا در ارسال تلگرام:", r.text)
    except Exception as e:
        print("❌ خطای عمومی تلگرام:", e)

if __name__ == "__main__":
    print("🚀 شروع اجرای فایل signal_bot.py")
    signals = generate_all_signals()
    if not signals:
        print("⚠️ هیچ سیگنالی دریافت نشد.")
    for signal in signals:
        signal_text = format_signal(signal)
        send_email(signal_text)
        send_telegram(signal_text)
    print("🏁 پایان اجرای فایل.")