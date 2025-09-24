import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

def get_price(symbol="BTCUSDT"):
    url = f"https://api.mexc.com/api/v3/ticker/price?symbol={symbol}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return float(r.json()["price"])
    except Exception as e:
        print("❌ خطا در دریافت قیمت:", e)
    return 0.0

def get_signal():
    print("📡 شروع دریافت سیگنال از API رندر...")
    url = "https://smart-signal-app-v2.onrender.com/signal?symbol=BTCUSDT&timeframe=1h"
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=20)
            print(f"📡 تلاش {attempt+1} | وضعیت پاسخ: {r.status_code}")
            if r.status_code == 200 and r.text.strip():
                data = r.json()
                if "symbol" in data and "technical" in data:
                    price = get_price(data["symbol"])
                    signal = {
                        "symbol": data["symbol"],
                        "action": data["technical"],
                        "entry": price,
                        "stop_loss": price * 0.995,
                        "take_profit": data["technical"] == "buy"
                    }
                    print("✅ سیگنال دریافت شد:", signal)
                    return [signal]
                else:
                    print("⚠️ داده‌ی ناقص دریافت شد:", data)
                    return []
            else:
                print("⚠️ پاسخ نامعتبر یا خالی بود.")
        except Exception as e:
            print(f"❌ تلاش {attempt+1} شکست خورد:", e)
            time.sleep(5)
    print("❌ همه تلاش‌ها برای دریافت سیگنال شکست خورد.")
    return []

def format_signal(signal):
    try:
        text = (
            f"📡 سیگنال جدید:\n"
            f"نماد: {signal['symbol']}\n"
            f"عملیات: {signal['action']}\n"
            f"ورود: {signal['entry']:.8f}\n"
            f"حد ضرر: {signal['stop_loss']:.8f}\n"
            f"{'✅ حد سود فعال' if signal['take_profit'] else '⏳ در انتظار حد سود'}"
        )
        print("🧾 متن سیگنال ساخته شد:\n", text)
        return text
    except Exception as e:
        print("❌ خطا در ساخت متن سیگنال:", e)
        return ""

def send_email(signal_text):
    print("📨 شروع ارسال ایمیل...")
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO") or email_user

    print("📤 ایمیل فرستنده:", email_user)
    print("📤 ایمیل گیرنده:", email_to)

    if not email_user or not email_pass:
        print("❌ متغیرهای EMAIL_USER یا EMAIL_PASS تعریف نشده‌اند.")
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
    print("📨 شروع ارسال تلگرام...")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("❌ متغیرهای تلگرام تعریف نشده‌اند.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": signal_text
    }

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
    signals = get_signal()
    if not signals:
        print("⚠️ هیچ سیگنالی دریافت نشد.")
    for signal in signals:
        signal_text = format_signal(signal)
        if not signal_text.strip():
            print("⚠️ متن سیگنال خالی بود، پیام ارسال نشد.")
            continue
        send_email(signal_text)
        send_telegram(signal_text)
    print("🏁 پایان اجرای فایل.")