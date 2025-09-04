import os

def check_files():
    print("🔍 بررسی فایل‌های کلیدی...")
    required_files = ["main.py", "requirements.txt", "render.yaml"]
    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print(f"❌ فایل‌های زیر پیدا نشدن: {missing}")
    else:
        print("✅ همه فایل‌های اصلی موجودن.")

def check_requirements():
    print("\n🔍 بررسی کتابخانه‌های ضروری...")
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            content = f.read().lower()
        required_libs = ["fastapi", "uvicorn", "pandas", "ta", "scikit-learn"]
        missing_libs = [lib for lib in required_libs if lib not in content]
        if missing_libs:
            print(f"⚠️ کتابخانه‌های زیر تو requirements.txt نیستن یا اشتباه نوشته شدن: {missing_libs}")
        else:
            print("✅ همه کتابخانه‌های لازم موجودن.")
    except FileNotFoundError:
        print("❌ فایل requirements.txt پیدا نشد.")

def check_structure():
    print("\n🔍 بررسی ساختار پوشه‌ها و فایل‌های داخلی...")
    expected_structure = {
        "analysis": ["technical.py", "ml_model.py"],
        "data": ["fetch_data.py"]
    }
    for folder, files in expected_structure.items():
        if not os.path.isdir(folder):
            print(f"❌ پوشه '{folder}' پیدا نشد.")
        else:
            for file in files:
                path = os.path.join(folder, file)
                if not os.path.exists(path):
                    print(f"❌ فایل '{path}' پیدا نشد.")
    print("✅ بررسی ساختار انجام شد.")

def check_render_yaml():
    print("\n🔍 بررسی فایل render.yaml...")
    try:
        with open("render.yaml", "r", encoding="utf-8") as f:
            content = f.read()
        if "startCommand" not in content or "uvicorn" not in content:
            print("⚠️ فایل render.yaml ممکنه ناقص باشه یا startCommand اشتباه تنظیم شده باشه.")
        else:
            print("✅ فایل render.yaml به نظر درست میاد.")
    except FileNotFoundError:
        print("❌ فایل render.yaml پیدا نشد.")

def main():
    print("🚀 شروع بررسی پروژه برای دیپلوی روی Render...\n")
    check_files()
    check_requirements()
    check_structure()
    check_render_yaml()
    print("\n✅ بررسی کامل شد. اگر خطایی دیدی، لطفاً رفعش کن و دوباره تست بگیر.")

if __name__ == "__main__":
    main()