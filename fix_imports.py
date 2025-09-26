import os

def replace_imports(root_dir, old_import, new_import):
    """
    جستجو در تمام فایل‌های .py و جایگزینی ایمپورت قدیمی با جدید.
    """
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(subdir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if old_import in content:
                    new_content = content.replace(old_import, new_import)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ اصلاح شد: {file_path}")

# مسیر پروژه
project_root = "C:/Users/It/Desktop/smartsignalbot"

# ایمپورت قدیمی و جدید
old = "from TradingApp.generate_signal import get_binance_data"
new = "from TradingApp.generate_signal import get_binance_data"

# اجرای اصلاح
replace_imports(project_root, old, new)