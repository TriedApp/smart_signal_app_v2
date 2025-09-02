@echo off
echo ✅ بررسی وجود فایل requirements.txt...
if not exist requirements.txt (
  echo 📦 ساخت فایل requirements.txt...
  echo fastapi>requirements.txt
  echo uvicorn>>requirements.txt
  echo pandas>>requirements.txt
  echo ta>>requirements.txt
  echo scikit-learn>>requirements.txt
)

echo ✅ نصب کتابخانه‌ها...
pip install -r requirements.txt

echo ✅ اجرای سرور...
uvicorn main:app --host 0.0.0.0 --port 10000
pause