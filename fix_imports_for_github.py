import os

target_file = "TradingApp/scripts/signal_bot.py"
fix_line = 'sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))\n'

# بررسی وجود فایل
if not os.path.exists(target_file):
    print("❌ فایل signal_bot.py پیدا نشد.")
    exit(1)

with open(target_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# بررسی اینکه آیا خط sys.path قبلاً اضافه شده
if any("sys.path.append" in line for line in lines):
    print("✅ مسیر ایمپورت قبلاً اصلاح شده.")
else:
    # پیدا کردن محل مناسب برای درج
    insert_index = None
    for i, line in enumerate(lines):
        if line.startswith("import") or line.startswith("from"):
            insert_index = i
            break

    # اضافه کردن اصلاح مسیر
    if insert_index is not None:
        lines.insert(insert_index, "import sys\nimport os\n" + fix_line)
        with open(target_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("✅ مسیر ایمپورت در signal_bot.py اصلاح شد.")
    else:
        print("❌ محل درج مناسب پیدا نشد.")