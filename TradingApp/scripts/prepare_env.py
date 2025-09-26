import os

# مسیر پروژه
project_root = r"C:\Users\It\Desktop\smartsignalbot\TradingApp"
env_file = os.path.join(project_root, ".env")
gitignore_file = os.path.join(project_root, ".gitignore")
env_example_file = os.path.join(project_root, ".env.example")

# حذف فایل .env از Git (بدون حذف فیزیکی)
os.system(f'git rm --cached "{env_file}"')

# افزودن .env به .gitignore
if os.path.exists(gitignore_file):
    with open(gitignore_file, "r+", encoding="utf-8") as f:
        lines = f.read().splitlines()
        if ".env" not in lines:
            f.write("\n.env\n")
else:
    with open(gitignore_file, "w", encoding="utf-8") as f:
        f.write(".env\n")

# ساخت فایل امن .env.example
example_content = """# .env.example
OPENAI_API_KEY=your_openai_key_here
HF_ACCESS_TOKEN=your_huggingface_token_here
TELEGRAM_TOKEN=your_telegram_token_here
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password
"""

with open(env_example_file, "w", encoding="utf-8") as f:
    f.write(example_content)

# کامیت تغییرات
os.system('git add .gitignore .env.example')
os.system('git commit -m "🔐 آماده‌سازی مقدماتی پروژه: حذف .env، افزودن به .gitignore، ساخت .env.example"')

print("✅ مرحله مقدماتی با موفقیت انجام شد. آماده‌ی دیپلوی هستی.")