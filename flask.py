import os

project_path = r"C:\Users\It\Desktop\TriedApp"

files_to_create = {
    "config.yaml": '''env: python
buildCommand: pip install -r requirements.txt
startCommand: python app.py
''',
    "runtime.txt": "python-3.10.12"
}

for filename, content in files_to_create.items():
    file_path = os.path.join(project_path, filename)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ فایل '{filename}' ساخته شد.")
    else:
        print(f"📁 فایل '{filename}' از قبل وجود دارد.")

print("\n🎯 فایل‌های پیکربندی با موفقیت بررسی و ساخته شدند.")