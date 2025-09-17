def send_alert(signal):
    if isinstance(signal, dict):
        print(f"🔔 هشدار سیگنال: {signal.get('type')} | ورود: {signal.get('entry')} | SL: {signal.get('stop_loss')}")
    elif isinstance(signal, tuple) and len(signal) >= 5:
        print(f"🔔 هشدار سیگنال: {signal[1]} | ورود: {signal[2]} | SL: {signal[3]}")
    else:
        print("⚠️ سیگنال نامعتبر دریافت شد.")
