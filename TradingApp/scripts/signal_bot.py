from TradingApp.scripts.multi_symbol_runner import generate_all_signals
from TradingApp.utils.notify import send_email, send_telegram
import os

def format_signal(symbol: str, signal_type: str) -> str:
    """
    قالب‌بندی سیگنال برای ارسال.
    """
    return (
        f"📡 سیگنال جدید\n"
        f"نماد: {symbol}\n"
        f"نوع: {'📈 خرید' if signal_type == 'buy' else '📉 فروش'}\n"
        f"ورود: 0.00000000\n"
        f"حد ضرر: 0.00000000\n"
        f"{'✅ حد سود فعال' if signal_type == 'buy' else '⏳ در انتظار حد سود'}"
    )

def main():
    print("🚀 شروع اجرای فایل signal_bot.py")

    # نمادهای مورد نظر برای تحلیل
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

    # اجرای تحلیل روی همه نمادها
    signals = generate_all_signals(symbols)

    # ساخت پیام نهایی
    all_messages = []
    for symbol, signal_type in signals.items():
        if signal_type:
            msg = format_signal(symbol, signal_type)
            print(f"\n✅ سیگنال برای {symbol}:\n{msg}")
            all_messages.append(msg)
        else:
            print(f"\n⏳ سیگنالی برای {symbol} یافت نشد.")

    # ارسال به ایمیل و تلگرام
    if all_messages:
        final_text = "\n\n".join(all_messages)
        send_email(final_text)
        send_telegram(final_text)
    else:
        print("⚠️ هیچ سیگنالی برای ارسال وجود ندارد.")

    print("🏁 پایان اجرای فایل.")

if __name__ == "__main__":
    main()