import requests

def test_mexc_api(symbol="BTCUSDT", interval="1d", limit=5):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    print(f"🔍 تست اتصال به: {url}")

    try:
        response = requests.get(url)
        print(f"📡 وضعیت پاسخ: {response.status_code}")

        if response.status_code != 200:
            print("❌ API پاسخ موفق نداد.")
            print("📄 متن پاسخ:", response.text)
            return

        try:
            data = response.json()
            print(f"✅ تعداد کندل دریافتی: {len(data)}")
            print("🕒 نمونه زمان کندل:", data[0][0])
            print("💰 قیمت بسته‌شدن:", data[0][4])
        except Exception as e:
            print("❌ خطا در تبدیل JSON:", e)
            print("📄 متن خام پاسخ:", response.text)

    except Exception as e:
        print("❌ خطا در اتصال به API:", e)

if __name__ == "__main__":
    test_mexc_api()