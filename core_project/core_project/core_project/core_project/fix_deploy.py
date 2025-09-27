import os

# مسیر فعلی اجرای اسکریپت
project_root = os.path.dirname(os.path.abspath(__file__))
req_path = os.path.join(project_root, "requirements.txt")
render_path = os.path.join(project_root, "render.yaml")

required_packages = {
    "fastapi",
    "uvicorn",
    "pandas",
    "scikit-learn",
    "numpy",
    "requests"
}

correct_render_yaml = '''services:
  - type: web
    name: smartsignalbot
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port=${PORT}"
    plan: free
    region: oregon
    branch: master
    autoDeploy: true
'''

def fix_requirements():
    if not os.path.exists(req_path):
        print("⚠️ فایل requirements.txt پیدا نشد. در حال ساخت فایل جدید...")
        with open(req_path, "w", encoding="utf-8") as f:
            for pkg in sorted(required_packages):
                f.write(f"{pkg}\n")
        print("✅ فایل requirements.txt ساخته شد.")
        return

    with open(req_path, "r", encoding="utf-8") as f:
        lines = set(line.strip() for line in f if line.strip())

    missing = required_packages - lines
    if missing:
        print(f"🔧 افزودن کتابخانه‌های ناقص به requirements.txt: {missing}")
        with open(req_path, "a", encoding="utf-8") as f:
            for pkg in missing:
                f.write(f"{pkg}\n")
    else:
        print("✅ فایل requirements.txt کامل است.")

def fix_render_yaml():
    if not os.path.exists(render_path):
        print("⚠️ فایل render.yaml پیدا نشد. در حال ساخت فایل جدید...")
        with open(render_path, "w", encoding="utf-8") as f:
            f.write(correct_render_yaml)
        print("✅ فایل render.yaml ساخته شد.")
        return

    with open(render_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "${PORT}" not in content or "autoDeploy: tru" in content or "port 10000" in content:
        print("🔧 اصلاح render.yaml برای استفاده از پورت دینامیک و رفع اشتباهات تایپی...")
        with open(render_path, "w", encoding="utf-8") as f:
            f.write(correct_render_yaml)
        print("✅ فایل render.yaml اصلاح شد.")
    else:
        print("✅ فایل render.yaml سالم است.")

def main():
    print(f"\n🔍 شروع بررسی و اصلاح فایل‌ها در مسیر: {project_root}")
    fix_requirements()
    fix_render_yaml()
    print("\n🎯 اصلاحات کامل شد. آماده‌ی دیپلوی هستی.")

if __name__ == "__main__":
    main()