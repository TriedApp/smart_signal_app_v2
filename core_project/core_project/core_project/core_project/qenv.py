import os

env_path = ".env"
key_name = "RENDER_API_KEY"
key_value = "rnd_odFPeSNBYX6Xo6RsOAr4e7aAH7vW"

def update_env_file(path, key, value):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"{key}={value}\n")
        print(f"✅ فایل جدید ساخته شد و {key} اضافه شد.")
        return

    with open(path, "r") as f:
        lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break

    if not updated:
        lines.append(f"{key}={value}\n")

    with open(path, "w") as f:
        f.writelines(lines)

    print(f"✅ کلید {'آپدیت شد' if updated else 'اضافه شد'} در فایل .env")

# اجرای تابع
update_env_file(env_path, key_name, key_value)