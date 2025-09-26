# 📦 ایمپورت‌های اصلی
import sys
import os

# 🛠 تنظیم مسیر برای اجرای صحیح در GitHub Actions یا Render
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 📡 ایمپورت توابع سیگنال و ارسال
from TradingApp.scripts.multi_symbol_runner import generate_all_signals
from TradingApp.utils.notify import send_email, send_telegram

# 🎨 قالب‌بندی سیگنال برای ارسال
def format_signal(signal: dict) -> str:
    return (
        f"📡 سیگنال جدید:\n"
        f"نماد: {signal['symbol']}\n"
        f"نوع: {'📈 خرید' if signal['technical'] == 'buy' else '📉 فروش'}\n"
        f"ورود: {signal.get('entry', '0.00000000')}\n"
        f"حد ضرر: {signal.get('stop_loss', '0.00000000')}\n"
        f"{'✅ حد سود فعال' if signal['technical'] == 'buy' else '⏳ در انتظار حد سود'}"
    )

# 🚀 نقطه شروع اجرای فایل
def main():
    print("🚀 شروع اجرای فایل signal_bot.py")

    # 🎯 نمادهای مورد نظر برای تحلیل
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

    # 📊 دریافت سیگنال‌ها
    signals = generate_all_signals(symbols)

    # 🧾 ساخت پیام نهایی
    all_messages = []
    for signal in signals:
        msg = format_signal(signal)
        print(f"\n{msg}")
        all_messages.append(msg)

    # 📤 ارسال به ایمیل و تلگرام
    if all_messages:
        final_text = "\n\n".join(all_messages)
        send_email(final_text)
        send_telegram(final_text)
    else:
        print("⚠️ هیچ سیگنالی برای ارسال وجود ندارد.")

    print("🏁 پایان اجرای فایل.")

# 🧨 اجرای مستقیم
if __name__ == "__main__":
    main()