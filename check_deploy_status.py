import os
import requests
from dotenv import load_dotenv

# مسیر دقیق فایل .env
env_path = r"C:\Users\It\Desktop\TriedApp\.env"
load_dotenv(dotenv_path=env_path)

# گرفتن مقادیر از فایل .env
service_id = os.getenv("RENDER_SERVICE_ID")
api_key = os.getenv("RENDER_API_KEY")

print("🚀 بررسی وضعیت دیپلوی و تست سرویس...")

# بررسی وجود شناسه سرویس
if not service_id:
    print("❌ شناسه سرویس یافت نشد. لطفاً مقدار RENDER_SERVICE_ID را در فایل .env وارد کنید.")
    exit(1)

# بررسی وجود کلید API
if not api_key:
    print("❌ کلید API برای Render یافت نشد. لطفاً مقدار RENDER_API_KEY را در فایل .env وارد کنید.")
    exit(1)

# ساخت URL برای بررسی دیپلوی
url = f"https://api.render.com/v1/services/{service_id}/deploys"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    if not data:
        print("⚠️ هیچ دیپلوی‌ای برای این سرویس ثبت نشده.")
        exit(0)

    latest_deploy = data[0]
    status = latest_deploy.get("status", "unknown")

    print(f"📦 وضعیت آخرین دیپلوی: {status}")

    if status == "live":
        print("✅ سرویس بالا اومده و live هست.")
    elif status == "failed":
        print("❌ دیپلوی با خطا مواجه شده.")
    else:
        print("⏳ دیپلوی هنوز کامل نشده یا در وضعیت نامشخصه.")
except requests.exceptions.RequestException as e:
    print(f"❌ خطا در اتصال به API Render: {e}")