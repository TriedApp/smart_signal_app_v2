import sys
import os

# 🛠 اضافه کردن مسیر root پروژه به sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.insert(0, project_root)

# 📡 ایمپورت توابع سیگنال و ارسال
from TradingApp.scripts.multi_symbol_runner import generate_all_signals
from TradingApp.utils.notify import send_email, send_telegram

def format_signal(signal: dict) -> str:
    return (
        f"📡 سیگنال جدید:\n"
        f"نماد: {signal['symbol']}\n"
        f"نوع: {'📈 خرید' if signal['technical'] == 'buy' else '📉 فروش'}\n"
        f"ورود: {signal.get('entry', '0.00000000')}\n"
        f"حد ضرر: {signal.get('stop_loss', '0.00000000')}\n"
        f"{'✅ حد سود فعال' if signal['technical'] == 'buy' else '⏳ در انتظار حد سود'}"
    )

def main():
    print("🚀 شروع اجرای فایل signal_bot.py")

    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    signals = generate_all_signals(symbols)

    all_messages = []
    for signal in signals:
        msg = format_signal(signal)
        print(f"\n{msg}")
        all_messages.append(msg)

    if all_messages:
        final_text = "\n\n".join(all_messages)
        send_email(final_text)
        send_telegram(final_text)
    else:
        print("⚠️ هیچ سیگنالی برای ارسال وجود ندارد.")

    print("🏁 پایان اجرای فایل.")

if __name__ == "__main__":
    main()