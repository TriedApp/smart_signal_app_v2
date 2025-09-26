import os
import smtplib
from email.message import EmailMessage

# دریافت متغیرهای محیطی
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

# بررسی اولیه
if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
    print("❌ یکی از متغیرهای محیطی ایمیل تعریف نشده. لطفاً EMAIL_USER، EMAIL_PASS و EMAIL_TO را بررسی کن.")
    exit(1)

# ساخت پیام ایمیل
msg = EmailMessage()
msg["Subject"] = "📡 تست ارسال ایمیل از SignalBot"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg.set_content("این یک ایمیل تستی است برای بررسی اتصال SMTP از طریق GitHub Actions یا لوکال.")

# تنظیمات SMTP (مثال: Yahoo)
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        print("✅ ایمیل تستی با موفقیت ارسال شد.")
except Exception as e:
    print("❌ خطا در ارسال ایمیل:")
    print(str(e))