def confirm_signal(signals):
    confirmed = []
    for signal in signals:
        if isinstance(signal, dict):
            if signal.get("confidence", 0) >= 0.8:
                confirmed.append(signal)
        elif isinstance(signal, tuple) and len(signal) >= 5:
            confirmed.append({
                "time": signal[0],
                "type": signal[1],
                "entry": signal[2],
                "stop_loss": signal[3],
                "take_profit_hit": signal[4]
            })
    return confirmed
