import os
import importlib.util

# مسیر فعلی پروژه
base_path = os.getcwd()

# لیست فایل‌ها و پوشه‌های مورد انتظار
expected_paths = [
    "main.py",
    "requirements.txt",
    os.path.join("analysis", "technical.py"),
    os.path.join("analysis", "ml_model.py"),
    os.path.join("data", "fetch_data.py")
]

print("🔍 بررسی ساختار پروژه در مسیر:", base_path)
for path in expected_paths:
    full_path = os.path.join(base_path, path)
    if os.path.exists(full_path):
        print(f"✅ پیدا شد: {path}")
    else:
        print(f"❌ پیدا نشد: {path}")

# بررسی وجود تابع get_signal در main.py
print("\n🔍 بررسی تابع get_signal در main.py:")
main_path = os.path.join(base_path, "main.py")
try:
    spec = importlib.util.spec_from_file_location("main", main_path)
    main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main)
    if hasattr(main, "get_signal"):
        print("✅ تابع get_signal پیدا شد.")
    else:
        print("❌ تابع get_signal پیدا نشد.")
except Exception as e:
    print(f"⚠️ خطا در بارگذاری main.py: {e}")