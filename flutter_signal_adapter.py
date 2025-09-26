import requests

def get_signal_for_flutter():
    url = "http://localhost:8000/signal"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            flutter_format = f"""
📡 سیگنال جدید برای اپلیکیشن:
ارز: {data['symbol']}
نوع سیگنال: {data['signal']}
نقطه ورود: {data['entry_price']}
نقطه خروج: {data['exit_price']}
اعتماد به تحلیل: {data['confidence'] * 100:.1f}%
"""
            print(flutter_format)
        else:
            print("⚠️ پاسخ نامعتبر از سرور")
    except Exception as e:
        print(f"❌ خطا در دریافت سیگنال: {e}")

if __name__ == "__main__":
    get_signal_for_flutter()