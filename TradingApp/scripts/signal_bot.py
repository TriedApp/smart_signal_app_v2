import asyncio
import aiohttp
import pandas as pd
import os
from TradingApp.utils.strategy import generate_signal
from TradingApp.utils.notify import send_email, send_telegram

TEST_MODE = True  # برای تست سریع، بعداً False کن

symbols = (
    ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    if TEST_MODE
    else [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
        "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT",
        "MATICUSDT", "LTCUSDT", "TRXUSDT", "ATOMUSDT", "OPUSDT",
        "INJUSDT", "RNDRUSDT", "ARBUSDT", "PEPEUSDT", "SUIUSDT"
    ]
)

interval = "1h"
save_path = "data/klines"
os.makedirs(save_path, exist_ok=True)

async def fetch_klines(session, symbol, interval):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
    try:
        async with session.get(url) as response:
            data = await response.json()
            if not isinstance(data, list) or not data:
                print(f"⚠️ دیتافریم خالی برای {symbol}")
                return symbol, None

            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_volume", "trades", "taker_buy_base",
                "taker_buy_quote", "ignore"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]
            df = df.astype(float, errors="ignore")

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