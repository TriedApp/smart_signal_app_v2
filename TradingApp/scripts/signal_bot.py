import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from signal_engine.generate_signal import get_mexc_data, run_strategy

def format_signal(signal):
    return (
        f"📡 سیگنال جدید:\n"
        f"نماد: {signal['symbol']}\n"
        f"عملیات: {signal['action']}\n"
        f"ورود: {signal['entry']:.8f}\n"
        f"حد ضرر: {signal['stop_loss']:.8f}\n"
        f"{'✅ حد سود فعال' if signal['take_profit'] else '⏳ در انتظار حد سود'}"
    )

def send_email(signal_text):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    if not email_user or not email_pass:
        print("❌ متغیرهای محیطی EMAIL_USER یا EMAIL_PASS تعریف نشده‌اند.")
        return

    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587

    print("📡 در حال استفاده از سرور:", smtp_server)

    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(email_user, email_pass)

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_user  # گیرنده می‌تونه تغییر کنه
        msg["Subject"] = "📈 سیگنال معاملاتی جدید"
        msg.attach(MIMEText(signal_text, "plain"))

        smtp.send_message(msg)
        smtp.quit()
        print("✅ ایمیل با موفقیت ارسال شد.")

    except smtplib.SMTPAuthenticationError as e:
        print("❌ خطای احراز هویت SMTP:", e)
    except smtplib.SMTPConnectError as e:
        print("❌ اتصال به سرور SMTP برقرار نشد:", e)
    except smtplib.SMTPException as e:
        print("❌ خطای SMTP:", e)
    except Exception as e:
        print("❌ خطای عمومی:", e)

if __name__ == "__main__":
    df = get_mexc_data()
    signals = run_strategy(df)
    for signal in signals:
        signal_text = format_signal(signal)
        send_email(signal_text)