import asyncio
import aiohttp
import pandas as pd

symbol = "BTC_USDT"
interval = "1h"

async def fetch_klines(session, symbol, interval):
    url = f"https://contract.mexc.com/api/v1/contract/kline?symbol={symbol}&interval={interval}&limit=100"
    try:
        async with session.get(url) as response:
            raw = await response.text()
            print(f"\n🔍 پاسخ خام از API برای {symbol}:\n{raw}\n")

            data = await response.json()
            klines = data.get("data", [])
            if not klines:
                print(f"⚠️ دیتافریم خالی برای {symbol}")
                return

            df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df = df.astype(float, errors="ignore")

            print(f"\n✅ دیتافریم نهایی برای {symbol}:\n{df.tail(3)}\n")

    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        await fetch_klines(session, symbol, interval)

if __name__ == "__main__":
    asyncio.run(main())