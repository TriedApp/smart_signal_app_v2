import os

# مسیرها
os.makedirs("TradingApp/scripts", exist_ok=True)
os.makedirs(".github/workflows", exist_ok=True)

# فایل strategy.py
with open("TradingApp/strategy.py", "w") as f:
    f.write("""<اینجا کد کامل strategy.py که قبلاً برات نوشتم قرار می‌گیره>""")

# فایل signal_bot_mexc.py
with open("TradingApp/scripts/signal_bot_mexc.py", "w") as f:
    f.write("""<اینجا کد کامل signal_bot_mexc.py که برای MEXC نوشتم قرار می‌گیره>""")

# فایل requirements.txt
with open("TradingApp/requirements.txt", "w") as f:
    f.write("pandas\nrequests\nschedule\n")

# فایل signal.yml
with open(".github/workflows/signal.yml", "w") as f:
    f.write("""name: Signal Dispatcher

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  send-signal:
    runs-on: ubuntu-latest

    steps:
      - name: 📥 دریافت کد پروژه
        uses: actions/checkout@v3

      - name: 🐍 تنظیم نسخه پایتون
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: 📦 نصب وابستگی‌ها
        run: pip install -r TradingApp/requirements.txt

      - name: 🚀 اجرای فایل سیگنال‌دهی
        run: |
          export PYTHONPATH=$(pwd)/TradingApp
          python TradingApp/scripts/signal_bot_mexc.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          EMAIL_USER: ${{ secrets.EMAIL_USER }}
          EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
""")

print("✅ پروژه آماده شد. حالا فقط دستورهای زیر رو اجرا کن:")
print("git add .")
print("git commit -m '🚀 افزودن ربات شکار سیگنال MEXC'")
print("git push")