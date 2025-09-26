import os

# مسیر فایل اجرایی
base_path = os.path.dirname(os.path.abspath(__file__))
req_path = os.path.join(base_path, "requirements.txt")

# محتوای مورد نیاز
required_packages = [
    "requests",
    "pandas",
    "ta"
]

# بررسی وجود فایل
if os.path.exists(req_path):
    print("✅ فایل requirements.txt از قبل وجود دارد.")
else:
    with open(req_path, "w") as f:
        f.write("\n".join(required_packages))
    print("📦 فایل requirements.txt ساخته شد و در کنار فایل اجرایی قرار گرفت.")