import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_email():
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    if not email_user or not email_pass:
        print("❌ متغیرهای محیطی EMAIL_USER یا EMAIL_PASS تعریف نشده‌اند.")
        return

    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(email_user, email_pass)

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_user
        msg["Subject"] = "✅ تست موفق اتصال SMTP از GitHub Actions"
        body = "این ایمیل تستی از طریق GitHub Actions ارسال شده است."
        msg.attach(MIMEText(body, "plain"))

        smtp.send_message(msg)
        smtp.quit()
        print("✅ ایمیل تستی با موفقیت ارسال شد.")

    except smtplib.SMTPAuthenticationError as e:
        print("❌ خطای احراز هویت SMTP:", e)
    except smtplib.SMTPConnectError as e:
        print("❌ اتصال به سرور SMTP برقرار نشد:", e)
    except smtplib.SMTPException as e:
        print("❌ خطای SMTP:", e)
    except Exception as e:
        print("❌ خطای عمومی:", e)

if __name__ == "__main__":
    send_test_email()