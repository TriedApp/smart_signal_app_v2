import os

project_path = "C:/Users/It/Desktop/smartsignalbot"
files_to_check = {
    "requirements.txt": ["fastapi", "uvicorn", "pandas", "ta", "scikit-learn"],
    "render.yaml": ["buildCommand", "startCommand"],
    "railway.json": ["start", "build"]
}

def check_file(filename, keywords):
    full_path = os.path.join(project_path, filename)
    if not os.path.exists(full_path):
        return f"❌ فایل {filename} وجود ندارد."
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [kw for kw in keywords if kw not in content]
    if missing:
        return f"⚠️ فایل {filename} ناقص است. موارد زیر یافت نشد: {missing}"
    return f"✅ فایل {filename} کامل و موجود است."

for fname, keys in files_to_check.items():
    result = check_file(fname, keys)
    print(result)