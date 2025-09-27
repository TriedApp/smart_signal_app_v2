@echo off
set PROJECT=C:\Users\It\Desktop\smartsignalbot
cd /d %PROJECT%

echo ✅ شروع Git init...
git init

echo ✅ اتصال به ریپوی GitHub...
git remote add origin https://github.com/TriedApp/smartsignal.git

echo ✅ اضافه کردن فایل‌ها...
git add .

echo ✅ کامیت تغییرات...
git commit -m "Initial commit for Render deploy"

echo ✅ پوش کردن به GitHub...
git push --set-upstream origin main

echo 🎯 حالا برو به Render و Manual Deploy رو بزن
pause