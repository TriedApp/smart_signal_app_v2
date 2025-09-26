import os

# مسیر فایل workflow
workflow_path = ".github/workflows/signal.yml"

# خطی که باید اضافه بشه
pythonpath_line = "      - name: 🛠 تنظیم مسیر ایمپورت‌ها (PYTHONPATH)\n        run: echo \"PYTHONPATH=$GITHUB_WORKSPACE\" >> $GITHUB_ENV\n"

# بررسی وجود فایل
if not os.path.exists(workflow_path):
    print("❌ فایل workflow پیدا نشد:", workflow_path)
    exit(1)

# خواندن محتوا
with open(workflow_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# بررسی اینکه آیا خط قبلاً اضافه شده یا نه
if any("PYTHONPATH" in line for line in lines):
    print("✅ خط PYTHONPATH قبلاً اضافه شده.")
else:
    # پیدا کردن محل مناسب برای درج خط (قبل از اجرای اسکریپت)
    insert_index = None
    for i, line in enumerate(lines):
        if "run: |" in line and "signal_bot.py" in lines[i + 1]:
            insert_index = i
            break

    if insert_index is not None:
        lines.insert(insert_index, pythonpath_line)
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("✅ خط PYTHONPATH با موفقیت اضافه شد.")
    else:
        print("❌ محل درج مناسب پیدا نشد.")