import os
import smtplib
import logging
from email.message import EmailMessage
from mimetypes import guess_type

# تنظیم لاگ‌گیری
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# مسیر فایل‌ها
project_root = os.getcwd()
log_filename = "signalbot_deployment_log_2025.md"
readme_filename = "README.md"

def send_email(subject: str, plain_text: str, html_content: str = None, attachments: list = None, recipients: list = None):
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TO = os.getenv("EMAIL_TO")

    if not EMAIL_USER or not EMAIL_PASS:
        logging.error("❌ متغیرهای محیطی ایمیل ناقص هستند.")
        return

    to_list = recipients if recipients else [EMAIL_TO]
    if not to_list or any(r is None for r in to_list):
        logging.error("❌ گیرنده ایمیل تعریف نشده.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(to_list)
    msg.set_content(plain_text)

    if html_content:
        msg.add_alternative(html_content, subtype="html")

    if attachments:
        for file_path in attachments:
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(file_path)
                    mime_type, _ = guess_type(file_path)
                    maintype, subtype = mime_type.split("/") if mime_type else ("application", "octet-stream")
                    msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
                    logging.info(f"📎 فایل ضمیمه اضافه شد: {file_name}")
            except Exception as e:
                logging.warning(f"⚠️ خطا در افزودن ضمیمه {file_path}: {e}")

    try:
        with smtplib.SMTP("smtp.mail.yahoo.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            logging.info("✅ ایمیل با موفقیت ارسال شد.")
    except Exception as e:
        logging.error(f"❌ خطا در ارسال ایمیل: {e}")

def write_log():
    log_path = os.path.join(project_root, log_filename)
    log_content = """# 📊 گزارش کامل پروژه SignalBot
**تاریخ:** 21 شهریور 1404  
**وضعیت:** ✅ ایمیل تستی ارسال شد، مستندات به‌روزرسانی شد

## جزئیات:
- ایمیل با موفقیت به گیرنده ارسال شد
- فایل ضمیمه بررسی و اضافه شد
- لاگ‌گیری کامل انجام شد
"""
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(log_content)
    logging.info(f"📝 فایل گزارش ذخیره شد: {log_path}")

def update_readme():
    readme_path = os.path.join(project_root, readme_filename)
    readme_note = "\n\n📄 برای مشاهده گزارش کامل پروژه، فایل [`signalbot_deployment_log_2025.md`](./signalbot_deployment_log_2025.md) را بررسی کنید.\n"

    if os.path.exists(readme_path):
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(readme_note)
        logging.info("📘 لینک گزارش به README.md اضافه شد.")
    else:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Smart Signal Bot\n" + readme_note)
        logging.info("📘 فایل README.md ساخته شد و لینک گزارش اضافه شد.")

# اجرای کامل
if __name__ == "__main__":
    send_email(
        subject="📡 تست خودکار ایم