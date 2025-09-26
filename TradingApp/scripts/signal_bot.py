import asyncio
import aiohttp
import pandas as pd
import os
from TradingApp.utils.strategy import generate_signal
from TradingApp.utils.notify import send_email, send_telegram

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT"
]

interval = "1h"
save_path = "data/klines"

os.makedirs(save_path, exist_ok=True)

async def fetch_klines(session, symbol, interval):
    url = f"https://contract.mexc.com/api/v1/klines?symbol={symbol}&interval={interval}&limit=100"
    try:
        async with session.get(url) as response:
            data = await response.json()
            klines = data.get("data", [])
            if not klines:
                print(f"⚠️ دیتافریم خالی برای {symbol}")
                return symbol, None

            df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df = df.astype(float, errors="ignore")

            # ذخیره‌سازی
            filename = f"{symbol}_{interval}.csv"
            df.to_csv(os.path.join(save_path, filename), index=False)

            return symbol, df
    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        return symbol, None

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_klines(session, symbol, interval) for symbol in symbols]
        results = await asyncio.gather(*tasks)

        for symbol, df in results:
            if df is None or df.empty:
                print(f"⏳ هیچ داده‌ای برای {symbol} یافت نشد.")
                continue

            df_dict = {interval: df}
            signal = generate_signal(df_dict, ai_trend="bullish", tf1h_trend="bullish")

            if signal:
                msg = (
                    f"📈 سیگنال {signal['type']} برای {symbol}\n"
                    f"🧠 شدت سیگنال: {signal['strength']}\n"
                    f"🛑 حد ضرر: {signal['stop']}\n"
                    f"🎯 حد سود: {signal['take_profit']}"
                )
                print(msg)
                send_email(msg)
                send_telegram(msg)
            else:
                print(f"⏳ هیچ سیگنالی برای {symbol} یافت نشد.")

if __name__ == "__main__":
    asyncio.run(main())