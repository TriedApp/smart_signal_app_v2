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
    path = "requirements.txt"
    if not os.path.exists(path):
        ensure_file(path, "\n".join(required_libs))
        return

    with open(path, "r+", encoding="utf-8") as f:
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
    path = "main.py"
    if not os.path.exists(path):
        content = """from fastapi import FastAPI
from analysis.technical import dummy_technical
from data.fetch_data import dummy_fetch

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SmartSignalBot is running!"}

@app.get("/technical")
def get_technical():
    return {"result": dummy_technical()}

@app.get("/data")
def get_data():
    return {"result": dummy_fetch()}
"""
        ensure_file(path, content)
    else:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "@app.get(\"/\")" not in content and "@app.get('/')\"" not in content:
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n\n@app.get(\"/\")\ndef read_root():\n    return {\"message\": \"SmartSignalBot is running!\"}")
            print("🔧 مسیر '/' به فایل main.py اضافه شد.")
        else:
            print("✅ مسیر '/' از قبل در فایل main.py تعریف شده.")

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

def create_internal_files():
    ensure_folder("analysis")
    ensure_folder("data")

    ensure_function("analysis/technical.py", "dummy_technical", "def dummy_technical():\n    return \"Technical analysis result\"")
    ensure_function("analysis/ml_model.py", "ml_model_placeholder", "# ML model placeholder")
    ensure_function("data/fetch_data.py", "dummy_fetch", "def dummy_fetch():\n    return \"Data fetch result\"")

def main():
    print("🚀 شروع آماده‌سازی خودکار پروژه برای دیپلوی روی Render...\n")
    update_requirements()
    create_render_yaml()
    create_main_py()
    create_internal_files()
    print("\n✅ همه چیز آماده‌ست! حالا می‌تونی پروژه رو کامیت کنی و دوباره دیپلوی بزنی.")

if __name__ == "__main__":
    main()