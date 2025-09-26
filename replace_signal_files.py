import os

# مسیرها
dispatcher_path = os.path.join("TradingApp", "scripts", "signal_dispatcher.py")
workflow_path = os.path.join(".github", "workflows", "signal.yml")

# محتوای فایل signal_dispatcher.py
dispatcher_code = '''<اینجا محتوای کامل فایل signal_dispatcher.py قرار می‌گیره>'''

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
      - name: 🛠 تنظیم مسیر ایمپورت‌ها
        run: echo "PYTHONPATH=$GITHUB_WORKSPACE" >> $GITHUB_ENV

      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install pandas numpy requests

      - name: Run signal dispatcher
        run: python TradingApp/scripts/signal_dispatcher.py
'''

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ فایل ذخیره شد: {path}")

# اجرای ساخت و جایگزینی
write_file(dispatcher_path, dispatcher_code)
write_file(workflow_path, workflow_code)