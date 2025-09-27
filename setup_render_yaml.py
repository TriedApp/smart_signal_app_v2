# setup_render_yaml.py
import os

yaml_content = """services:
  - type: web
    name: signal-bot
    env: python
    rootDir: smart_signal_app_v2
    buildCommand: pip install -r requirements.txt
    startCommand: python TradingApp/scripts/signal_bot.py
    autoDeploy: true
"""

file_path = os.path.join(os.getcwd(), ".render.yaml")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(yaml_content)

print("✅ فایل .render.yaml با موفقیت ساخته شد.")