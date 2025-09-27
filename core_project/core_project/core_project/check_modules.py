import os

def ensure_function(file_path, function_name, function_code):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(function_code)
        print(f"📄 فایل '{file_path}' ساخته شد و تابع '{function_name}' اضافه شد.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if function_name in content:
        print(f"✅ تابع '{function_name}' از قبل در فایل '{file_path}' وجود داره.")
    else:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n\n" + function_code)
        print(f"🔧 تابع '{function_name}' به فایل '{file_path}' اضافه شد.")

def main():
    print("🚀 بررسی و اصلاح فایل‌های تحلیل و داده...\n")

    technical_path = os.path.join("analysis", "technical.py")
    fetch_path = os.path.join("data", "fetch_data.py")

    dummy_technical_code = """def dummy_technical():
    return "Technical analysis result"
"""

    dummy_fetch_code = """def dummy_fetch():
    return "Data fetch result"
"""

    ensure_function(technical_path, "dummy_technical", dummy_technical_code)
    ensure_function(fetch_path, "dummy_fetch", dummy_fetch_code)

    print("\n✅ بررسی کامل شد. حالا می‌تونی دوباره `main.py` رو اجرا کنی.")

if __name__ == "__main__":
    main()