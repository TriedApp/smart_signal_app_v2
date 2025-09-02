@echo off
set PROJECT=C:\Users\It\Desktop\smartsignalbot
cd /d %PROJECT%

echo ✅ بررسی وجود فایل requirements.txt...
if not exist requirements.txt (
  echo fastapi>requirements.txt
  echo uvicorn>>requirements.txt
  echo pandas>>requirements.txt
  echo ta>>requirements.txt
  echo scikit-learn>>requirements.txt
)

echo ✅ بررسی وجود ریپو Git...
if not exist ".git" (
  git init
  git remote add origin https://github.com/TriedApp/smartsignal.git
)

echo ✅ اضافه کردن فایل‌ها...
git add .

echo ✅ کامیت تغییرات...
git commit -m "Fix: add requirements.txt for Render build"

echo ✅ پوش کردن به GitHub...
git push --set-upstream origin main

echo 🎯 حالا برو به Render و Manual Deploy رو بزن
echo ✅ گزینه 'Deploy latest commit' رو انتخاب کن
pause