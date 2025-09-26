import os

# مسیر پروژه
project_root = r"C:\Users\It\Desktop\smartsignalbot\TradingApp"
requirements_path = os.path.join(project_root, "requirements.txt")
render_yaml_path = os.path.join(project_root, "render.yaml")

# محتوای فایل requirements.txt
requirements = """fastapi
uvicorn
requests
python-dotenv
openai
transformers
smtplib
email-validator
"""

# محتوای فایل render.yaml
render_yaml = """services:
  - type: web
    name: smart-signal-app
    env: python
    plan: starter
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port 10000"
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: HF_API_KEY
        sync: false
      - key: TELEGRAM_TOKEN
        sync: false
      - key: EMAIL_USER
        sync: false
      - key: EMAIL_PASS
        sync: false
"""

# ساخت فایل‌ها
with open(requirements_path, "w", encoding="utf-8") as f:
    f.write(requirements)

with open(render_yaml_path, "w", encoding="utf-8") as f:
    f.write(render_yaml)

# افزودن و کامیت به Git
os.system(f'git add "{requirements_path}" "{render_yaml_path}"')
os.system('git commit -m "🚀 ساخت requirements.txt و render.yaml برای دیپلوی اتوماتیک"')

print("✅ مرحله دوم با موفقیت انجام شد. آماده‌ی دیپلوی روی Render هستی.")