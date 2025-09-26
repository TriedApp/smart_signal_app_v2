import os

workflow_path = ".github/workflows/signal.yml"
os.makedirs(os.path.dirname(workflow_path), exist_ok=True)

# بلوک کامل workflow
default_workflow = """name: Signal Dispatcher

on:
  workflow_dispatch:

jobs:
  send-signal:
    runs-on: ubuntu-latest

    env:
      EMAIL_USER: ${{ secrets.EMAIL_USER }}
      EMAIL_PASS: ${{ secrets.EMAIL_PASS }}

    steps:
      - name: 📥 دریافت سورس پروژه
        uses: actions/checkout@v3

      - name: 🐍 نصب پایتون
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: 🛠 تنظیم مسیر ایمپورت‌ها (PYTHONPATH)
        run: echo "PYTHONPATH=$GITHUB_WORKSPACE" >> $GITHUB_ENV

      - name: 📦 نصب وابستگی‌ها
        run: |
          pip install pandas numpy requests

      - name: 🚀 اجرای فایل signal_bot.py
        run: |
          echo "📡 اجرای فایل signal_bot.py از مسیر صحیح"
          python TradingApp/scripts/signal_bot.py
"""

# اگر فایل وجود نداشت، بسازش
if not os.path.exists(workflow_path):
    with open(workflow_path, "w", encoding="utf-8") as f:
        f.write(default_workflow)
    print("✅ فایل workflow ساخته شد با تنظیمات کامل.")
else:
    # اگر فایل وجود داشت، بررسی و اصلاح کن
    with open(workflow_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # اضافه کردن PYTHONPATH اگر نبود
    if "PYTHONPATH=$GITHUB_WORKSPACE" not in content:
        insert_point = content.find("steps:")
        if insert_point != -1:
            content = content.replace(
                "steps:",
                "steps:\n      - name: 🛠 تنظیم مسیر ایمپورت‌ها (PYTHONPATH)\n        run: echo \"PYTHONPATH=$GITHUB_WORKSPACE\" >> $GITHUB_ENV"
            )
            modified = True
            print("✅ خط PYTHONPATH اضافه شد.")

    # اصلاح مسیر اجرای فایل اگر اشتباه بود
    if "python TradingApp/signal_bot.py" in content:
        content = content.replace(
            "python TradingApp/signal_bot.py",
            "python TradingApp/scripts/signal_bot.py"
        )
        modified = True
        print("✅ مسیر اجرای signal_bot.py اصلاح شد.")

    if modified:
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ فایل workflow با موفقیت اصلاح شد.")
    else:
        print("✅ فایل workflow قبلاً کامل و صحیح بوده.")
