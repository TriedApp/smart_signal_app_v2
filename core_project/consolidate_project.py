import os
import shutil
from pathlib import Path
from filecmp import cmp

# مسیر پایه (جایی که اسکریپت اجرا می‌شه)
BASE_DIR = Path(__file__).resolve().parent

# پوشه‌ی مرکزی هدف
TARGET_DIR = BASE_DIR / "core_project"
TARGET_DIR.mkdir(exist_ok=True)

# پوشه‌های پراکنده‌ای که باید بررسی بشن
SOURCE_DIRS = [
    BASE_DIR,
    BASE_DIR.parent / "smartsignalbot",
    BASE_DIR.parent / "thirdapp"
]

# فایل‌هایی که قبلاً منتقل شدن
tracked_files = {}

print("🔍 شروع بررسی پوشه‌ها و فایل‌های تکراری...\n")

for src_dir in SOURCE_DIRS:
    if not src_dir.exists():
        print(f"⚠️ پوشه پیدا نشد: {src_dir}")
        continue

    for file in src_dir.glob("**/*"):
        if file.is_file() and not file.name.endswith(".bak"):
            rel_path = file.relative_to(src_dir)
            target_path = TARGET_DIR / rel_path

            # اگر فایل قبلاً منتقل شده
            if rel_path in tracked_files:
                existing = tracked_files[rel_path]
                if cmp(file, existing, shallow=False):
                    print(f"🔁 فایل تکراری و یکسان: {rel_path}")
                    continue
                else:
                    # فایل مشابه ولی متفاوت → ذخیره با پسوند alt
                    alt_path = TARGET_DIR / f"{rel_path.stem}_alt{rel_path.suffix}"
                    alt_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, alt_path)
                    print(f"⚠️ فایل مشابه ولی متفاوت: {rel_path} → ذخیره به عنوان {alt_path.name}")
            else:
                # فایل جدید → انتقال
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target_path)
                tracked_files[rel_path] = target_path
                print(f"📦 انتقال فایل: {rel_path}")

print("\n✅ همه‌ی فایل‌ها در پوشه core_project جمع‌آوری شدن.")
print("📁 حالا فقط از مسیرهای داخل core_project استفاده کن و فایل‌های قدیمی رو آرشیو یا حذف کن.")