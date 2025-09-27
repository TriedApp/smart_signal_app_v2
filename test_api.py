import requests

url = "https://api.mexc.com/api/v3/klines"
params = {
    "symbol": "BTCUSDT",
    "interval": "15m",
    "limit": 100
}

response = requests.get(url, params=params)
print("🔍 وضعیت پاسخ:", response.status_code)
print("📦 محتوا:", response.text[:300])