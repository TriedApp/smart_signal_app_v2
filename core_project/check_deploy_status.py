import os
import requests
from dotenv import load_dotenv

load_dotenv()

RENDER_API_KEY = os.getenv("RENDER_API_KEY")
RENDER_SERVICE_ID = os.getenv("RENDER_SERVICE_ID")
RENDER_SERVICE_URL = os.getenv("RENDER_SERVICE_URL")

headers = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Accept": "application/json"
}

def check_render_status():
    url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/deploys"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ خطا در اتصال به API Render:", response.text)
        return False

    deploys = response.json()
    latest = deploys["data"][0] if deploys["data"] else None

    if not latest:
        print("⚠️ هیچ دیپلوی‌ای پیدا نشد.")
        return False

    status = latest["status"]
    print(f"📦 وضعیت آخرین دیپلوی: {status}")

    return status == "live"

def test_service():
    try:
        response = requests.get(RENDER_SERVICE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ سرویس بالا اومده و پاسخ می‌ده:", response.json())
        else:
            print(f"⚠️ سرویس پاسخ داد ولی با status code: {response.status_code}")
    except Exception as e:
        print("❌ سرویس در دسترس نیست:", str(e))

if __name__ == "__main__":
    print("🚀 بررسی وضعیت دیپلوی و تست سرویس...")
    if check_render_status():
        test_service()
    else:
        print("❌ دیپلوی هنوز live نشده یا با خطا مواجه شده.")