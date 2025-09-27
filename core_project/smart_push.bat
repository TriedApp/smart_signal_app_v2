@echo off
echo 🔧 در حال بررسی تنظیمات Git...

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

REM بررسی وجود فایل‌های مورد نیاز
IF NOT EXIST "main.py" (
    echo ❌ فایل main.py پیدا نشد!
    goto end
)
IF NOT EXIST "requirements.txt" (
    echo ❌ فایل requirements.txt پیدا نشد!
    goto end
)

REM حذف فایل‌های غیرموجود از لیست
SET FILES=main.py requirements.txt
IF EXIST "render.yaml" SET FILES=%FILES% render.yaml
IF EXIST "railway.json" SET FILES=%FILES% railway.json

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

REM اضافه کردن فایل‌ها
git add %FILES%
git commit -m "Smart initial commit"

REM تنظیم branch و پوش
git branch -M main
git push -u origin main

:end
echo ✅ عملیات تمام شد. پنجره را ببند یا Enter بزن.
pause