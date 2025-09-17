import os
import requests
from dotenv import load_dotenv

# مرحله ۱: بارگذاری کلید از فایل .env
load_dotenv()
API_KEY = os.getenv("RENDER_API_KEY")

if not API_KEY:
    raise EnvironmentError("❌ کلید RENDER_API_KEY در فایل .env پیدا نشد!")

# مرحله ۲: تنظیمات دیپلوی
SERVICE_ID = "srv-d2s5oummcj7s73ft338g"  # شناسه سرویس FastAPI در Render
DEPLOY_ENDPOINT = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def trigger_deploy():
    print("🚀 ارسال درخواست دیپلوی به Render...")
    response = requests.post(DEPLOY_ENDPOINT, headers=HEADERS)

    if response.status_code == 201:
        deploy_id = response.json().get("id")
        print(f"✅ دیپلوی آغاز شد. شناسه دیپلوی: {deploy_id}")
        return deploy_id
    else:
        print(f"❌ خطا در دیپلوی: {response.status_code} - {response.text}")
        return None

def check_deploy_status(deploy_id):
    status_url = f"{DEPLOY_ENDPOINT}/{deploy_id}"
    print("⏳ بررسی وضعیت دیپلوی...")

    response = requests.get(status_url, headers=HEADERS)
    if response.status_code == 200:
        status = response.json().get("status")
        print(f"📦 وضعیت فعلی دیپلوی: {status}")
        return status
    else:
        print(f"❌ خطا در دریافت وضعیت: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    deploy_id = trigger_deploy()
    if deploy_id:
        import time
        for _ in range(10):
            status = check_deploy_status(deploy_id)
            if status in ["live", "failed"]:
                break
            time.sleep(5)