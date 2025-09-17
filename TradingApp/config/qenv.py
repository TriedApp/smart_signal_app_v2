import os
from dotenv import load_dotenv

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("✅ تنظیمات محیطی بارگذاری شد.")
    else:
        raise FileNotFoundError(f".env file not found at {env_path}")
