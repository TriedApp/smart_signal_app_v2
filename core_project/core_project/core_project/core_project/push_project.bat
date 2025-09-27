@echo off
echo 🔧 بررسی تنظیمات Git...

REM تنظیم نام و ایمیل اگر قبلاً ست نشده باشه
git config --get user.name >nul 2>&1
IF ERRORLEVEL 1 (
    git config --global user.name "Amir"
    echo ✅ نام کاربری تنظیم شد: Amir
)

git config --get user.email >nul 2>&1
IF ERRORLEVEL 1 (
    git config --global user.email "amir@example.com"
    echo ✅ ایمیل تنظیم شد: amir@example.com
)

REM شروع عملیات Git
echo 🚀 شروع پوش پروژه...
git init

REM بررسی وجود remote
git remote get-url origin >nul 2>&1
IF ERRORLEVEL 1 (
    git remote add origin https://github.com/TriedApp/smartsignalbot.git
) ELSE (
    git remote set-url origin https://github.com/TriedApp/smartsignalbot.git
)

REM اضافه کردن همه فایل‌های موجود
git add .
git commit -m "Smart initial commit"

REM تنظیم branch و پوش
git branch -M main
git push -u origin main

echo ✅ پروژه با موفقیت پوش شد!
pause