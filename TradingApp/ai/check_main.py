import os

main_path = os.path.join(os.getcwd(), "main.py")

required_code = """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SmartSignalBot is running!"}
"""

def check_and_update_main():
    if os.path.exists(main_path):
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "@app.get(\"/\")" in content or "@app.get('/')\"" in content:
            print("✅ مسیر '/' از قبل در فایل main.py تعریف شده.")
        else:
            with open(main_path, "a", encoding="utf-8") as f:
                f.write("\n\n" + required_code)
            print("🔧 مسیر '/' به فایل main.py اضافه شد.")
    else:
        print("❌ فایل main.py پیدا نشد.")

if __name__ == "__main__":
    check_and_update_main()