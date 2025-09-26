import os

# مسیرهای پروژه
project_root = r"C:\Users\It\Desktop\smartsignalbot\TradingApp"
workflow_dir = os.path.join(project_root, ".github", "workflows")
signal_script_path = os.path.join(project_root, "signal_bot.py")
workflow_file_path = os.path.join(workflow_dir, "signal.yml")

# ساخت پوشه workflow اگر وجود نداشت
os.makedirs(workflow_dir, exist_ok=True)

# محتوای فایل signal_bot.py
signal_bot_code = '''import requests
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
'''

# محتوای فایل signal.yml
workflow_code = '''name: Signal Dispatcher

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  run-signal:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests

      - name: Run signal script
        run: python signal_bot.py
'''

# نوشتن فایل‌ها
with open(signal_script_path, "w", encoding="utf-8") as f:
    f.write(signal_bot_code)

with open(workflow_file_path, "w", encoding="utf-8") as f:
    f.write(workflow_code)

# افزودن به Git و کامیت
os.system(f'git add "{signal_script_path}" "{workflow_file_path}"')
os.system('git commit -m "🚀 افزودن فایل‌های سیگنال‌دهی خودکار با GitHub Actions"')

print("✅ فایل‌ها ساخته شدند و آماده‌ی push به ریپو هستی.")