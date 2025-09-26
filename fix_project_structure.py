import os
import shutil

# مسیرهای اصلی
project_root = os.getcwd()
signal_engine_dir = os.path.join(project_root, "signal_engine")
generate_signal_filename = "generate_signal.py"
init_file = os.path.join(signal_engine_dir, "__init__.py")
signal_bot_path = os.path.join(project_root, "TradingApp", "scripts", "signal_bot.py")

# مرحله 1: ساخت پوشه signal_engine اگر وجود نداره
os.makedirs(signal_engine_dir, exist_ok=True)

# مرحله 2: ساخت فایل __init__.py اگر وجود نداره
if not os.path.exists(init_file):
    with open(init_file, "w", encoding="utf-8") as f:
        f.write("# Created automatically to define signal_engine as a package\n")
    print("✅ فایل __init__.py ساخته شد.")
else:
    print("✅ فایل __init__.py قبلاً وجود داشته.")

# مرحله 3: پیدا کردن فایل generate_signal.py در مسیر اشتباه
found_path = None
for root, dirs, files in os.walk(project_root):
    if generate_signal_filename in files:
        full_path = os.path.join(root, generate_signal_filename)
        if os.path.abspath(full_path).startswith(os.path.abspath(signal_engine_dir)):
            print("✅ فایل generate_signal.py در مسیر صحیح قرار دارد.")
        else:
            found_path = full_path
            break

# انتقال فایل به signal_engine
if found_path:
    target_path = os.path.join(signal_engine_dir, generate_signal_filename)
    shutil.move(found_path, target_path)
    print(f"✅ فایل {generate_signal_filename} منتقل شد به signal_engine/")
elif not os.path.exists(os.path.join(signal_engine_dir, generate_signal_filename)):
    print("⚠️ فایل generate_signal.py پیدا نشد. لطفاً بررسی کن که وجود داشته باشه.")

# مرحله 4: اصلاح مسیر ایمپورت در signal_bot.py
if not os.path.exists(signal_bot_path):
    print("❌ فایل signal_bot.py پیدا نشد.")
else:
    with open(signal_bot_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False

    # اضافه کردن sys.path اگر نبود
    if not any("sys.path.append" in line for line in lines):
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith("from") or line.startswith("import"):
                insert_index = i
                break
        lines.insert(insert_index, "import sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))\n")
        modified = True
        print("✅ مسیر ایمپورت در signal_bot.py اضافه شد.")

    # اصلاح ایمپورت signal_engine.generate_signal
    for i, line in enumerate(lines):
        if "from signal_engine" in line and "generate_signal" not in line:
            lines[i] = "from signal_engine.generate_signal import get_mexc_data, run_strategy\n"
            modified = True
            print("✅ ایمپورت signal_engine.generate_signal اصلاح شد.")

    if modified:
        with open(signal_bot_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("✅ فایل signal_bot.py با موفقیت اصلاح شد.")
    else:
        print("✅ فایل signal_bot.py قبلاً صحیح بوده.")