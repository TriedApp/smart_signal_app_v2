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

echo ✅ اضافه کردن فایل‌ها به Git...
git add .

echo ✅ کامیت تغییرات...
git commit -m "Fix: add requirements.txt for Render build"

echo ✅ پوش کردن به GitHub...
git push

echo.
echo 🎯 حالا برو به Render و روی Manual Deploy کلیک کن
echo ✅ گزینه 'Deploy latest commit' رو انتخاب کن و منتظر بیلد باش
pause