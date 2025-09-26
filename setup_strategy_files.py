import os

# --- کد strategy.py ---
strategy_code = """[کد کامل استراتژی که قبلاً ساختیم]"""

# --- کد multi_symbol_runner.py با ارسال ایمیل و تلگرام ---
runner_code = """[کد کامل نسخه‌ی چند نمادی با ارسال که قبلاً ساختیم]"""

# --- ساخت مسیرها ---
os.makedirs("TradingApp/scripts", exist_ok=True)

# --- نوشتن فایل‌ها ---
with open("TradingApp/strategy.py", "w", encoding="utf-8") as f:
    f.write(strategy_code.strip())

with open("TradingApp/scripts/multi_symbol_runner.py", "w", encoding="utf-8") as f:
    f.write(runner_code.strip())

print("✅ فایل‌ها ساخته شدند و آماده اجرا هستند.")