@echo off
cd /d C:\Users\It\Desktop\smartsignalbot

echo ✅ بررسی و اضافه کردن فایل‌ها...
git add .

echo ✅ کامیت تغییرات...
git commit -m "Add requirements.txt and fix for Render build"

echo ✅ پوش کردن به GitHub...
git push --set-upstream origin main

echo 🎯 حالا برو به Render و Manual Deploy رو بزن
pause