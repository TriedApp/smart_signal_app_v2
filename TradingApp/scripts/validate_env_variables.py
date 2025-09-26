import requests

# مقادیر فعلی برای بررسی
API_KEY = "rnd_odFPeSNBYX6Xo6RsOAr4e7aAH7vW"
RENDER_SERVICE_ID = "srv-d2s5oummcj7s73ft338g"
API_URL = "https://smartsignal.onrender.com/signal"

# بررسی API_KEY با ارسال درخواست تست
def test_api_key():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ API_KEY معتبر است و پاسخ دریافت شد.")
        else:
            print(f"⚠️ API_KEY نامعتبر یا endpoint پاسخ نداد. کد وضعیت: {response.status_code}")
    except Exception as e:
        print(f"❌ خطا در اتصال به API: {e}")

# بررسی API_URL بدون احراز هویت
def test_api_url():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            print("✅ API_URL فعال است و پاسخ می‌دهد.")
        else:
            print(f"⚠️ API_URL فعال نیست یا پاسخ نداد. کد وضعیت: {response.status_code}")
    except Exception as e:
        print(f"❌ خطا در اتصال به API_URL: {e}")

# بررسی RENDER_SERVICE_ID با ساختار اولیه
def test_render_service_id():
    if RENDER_SERVICE_ID.startswith("srv-") and len(RENDER_SERVICE_ID) > 10:
        print("✅ ساختار RENDER_SERVICE_ID معتبر است. برای اطمینان، با داشبورد Render مقایسه کن.")
    else:
        print("⚠️ RENDER_SERVICE_ID نامعتبر یا ناقص است.")

# اجرای تست‌ها
print("🔍 بررسی اعتبار متغیرهای محیطی:")
test_api_key()
test_api_url()
test_render_service_id()