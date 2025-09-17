from fastapi import FastAPI
from core.strategy import run_strategies
from ai.confirmation import confirm_signal
from alerts.dispatch import send_alert
from config.qenv import load_env
import uvicorn

app = FastAPI(title="SmartSignal API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/signals")
def get_signals():
    raw_signals = run_strategies()
    confirmed = confirm_signal(raw_signals)
    for signal in confirmed:
        send_alert(signal)
    return {"status": "success", "confirmed_signals": confirmed}

if __name__ == "__main__":
    try:
        load_env()
    except Exception as e:
        print(f"⚠️ خطا در بارگذاری تنظیمات محیطی: {e}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
