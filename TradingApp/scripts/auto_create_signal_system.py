import os

# مسیرهای پروژه
project_root = os.path.dirname(os.path.abspath(__file__)).replace("\\scripts", "")
workflow_dir = os.path.join(project_root, ".github", "workflows")
signal_script_path = os.path.join(project_root, "signal_bot.py")
workflow_file_path = os.path.join(workflow_dir, "signal.yml")

# ساخت پوشه workflow اگر وجود نداشت
os.makedirs(workflow_dir, exist_ok=True)

# محتوای فایل signal_bot.py
signal_bot_code = '''from dotenv import load_dotenv
import os
import requests
import smtplib
from email.mime.text import MIMEText

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

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
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

def send_email(msg):
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(EMAIL_USER, EMAIL_PASS)
    smtp.sendmail(EMAIL_USER, EMAIL_TO, MIMEText(msg))
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

env:
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
  EMAIL_USER: ${{ secrets.EMAIL_USER }}
  EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
  EMAIL_TO: ${{ secrets.EMAIL_TO }}

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
        run: pip install requests python-dotenv

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
os.system('git commit -m "🚀 ساخت فایل‌های سیگنال‌دهی هماهنگ با .env و GitHub Secrets"')

print("✅ فایل‌ها ساخته شدند و آماده‌ی push هستی.")