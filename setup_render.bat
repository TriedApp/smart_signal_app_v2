import os

def ensure_file(path, content=""):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ فایل '{path}' ساخته شد.")
    else:
        print(f"📄 فایل '{path}' از قبل وجود داره.")

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"📁 پوشه '{path}' ساخته شد.")
    else:
        print(f"📁 پوشه '{path}' از قبل وجود داره.")

def update_requirements():
    required_libs = ["fastapi", "uvicorn", "pandas", "ta", "scikit-learn"]
    if not os.path.exists("requirements.txt"):
        ensure_file("requirements.txt", "\n".join(required_libs))
        return

    with open("requirements.txt", "r+", encoding="utf-8") as f:
        content = f.read().lower()
        missing = [lib for lib in required_libs if lib not in content]
        if missing:
            f.write("\n" + "\n".join(missing))
            print(f"✅ کتابخانه‌های زیر به requirements.txt اضافه شدن: {missing}")
        else:
            print("✅ همه کتابخانه‌های لازم از قبل موجود بودن.")

def create_render_yaml():
    content = """services:
  - type: web
    name: smartsignalbot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port 10000
    plan: free
"""
    ensure_file("render.yaml", content)

def create_main_py():
    content = """from fastapi import FastAPI
from analysis.technical import dummy_technical
from data.fetch_data import dummy_fetch

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SmartSignalBot is running!"}
"""
    ensure_file("main.py", content)

def create_dummy_files():
    ensure_folder("analysis")
    ensure_file("analysis/technical.py", "def dummy_technical():\n    return 'Technical analysis placeholder'\n")

    ensure_file("analysis/ml_model.py", "# ML model placeholder\n")

    ensure_folder("data")
    ensure_file("data/fetch_data.py", "def dummy_fetch():\n    return 'Data fetch placeholder'\n")

def main():
    print("🚀 شروع آماده‌سازی خودکار پروژه برای دیپلوی روی Render...\n")
    update_requirements()
    create_render_yaml()
    create_main_py()
    create_dummy_files()
    print("\n✅ همه چیز آماده‌ست! حالا می‌تونی پروژه رو دیپلوی کنی یا اسکریپت بررسی رو دوباره اجرا کنی.")

if __name__ == "__main__":
    main()