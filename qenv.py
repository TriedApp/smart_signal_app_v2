import os
from dotenv import load_dotenv

# مسیر دقیق فایل .env روی دسکتاپ
env_path = r"C:\Users\It\Desktop\TriedApp\.env"

# بارگذاری فایل .env
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
    print(f"✅ فایل .env با موفقیت بارگذاری شد از مسیر:\n{env_path}")
else:
    print(f"❌ فایل .env پیدا نشد در مسیر:\n{env_path}")
    exit()

# بررسی مقدار RENDER_API_KEY
render_api_key = os.getenv("RENDER_API_KEY")

if render_api_key:
    print(f"🔑 مقدار RENDER_API_KEY پیدا شد:\n{render_api_key}")
else:
    print("🚫 مقدار RENDER_API_KEY در فایل .env تعریف نشده یا درست بارگذاری نشده.")
    print("🛠 لطفاً بررسی کن که کلید به‌صورت دقیق نوشته شده باشه: RENDER_API_KEY=value")