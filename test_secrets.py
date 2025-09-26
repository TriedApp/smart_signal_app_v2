import os

def test_secrets():
    secrets = {
        "EMAIL_USER": os.getenv("EMAIL_USER"),
        "EMAIL_PASS": os.getenv("EMAIL_PASS"),
        "EMAIL_TO": os.getenv("EMAIL_TO"),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID")
    }

    for key, value in secrets.items():
        if value:
            print(f"✅ {key} بارگذاری شد: {value[:5]}...")  # فقط ابتدای مقدار برای امنیت
        else:
            print(f"❌ {key} تعریف نشده یا بارگذاری نشده.")

if __name__ == "__main__":
    test_secrets()