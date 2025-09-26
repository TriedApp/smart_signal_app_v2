import os

# مسیرهای هدف
paths = [
    "TradingApp",
    "TradingApp/scripts"
]

for path in paths:
    init_file = os.path.join(path, "__init__.py")
    if not os.path.exists(init_file):
        os.makedirs(path, exist_ok=True)
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("# Initializer for Python package\n")
        print(f"✅ ساخته شد: {init_file}")
    else:
        print(f"ℹ️ قبلاً وجود داشته: {init_file}")