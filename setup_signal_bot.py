import os

base = os.path.abspath(os.path.dirname(__file__))
folders = ["TradingApp/scripts", "TradingApp/utils"]
files = {
    "requirements.txt": "requests\npandas\nnumpy\nta-lib\n",
    "TradingApp/utils/data.py": """import requests,pandas as pd
def get_mexc_klines(s,i='1h',l=100):
 u=f"https://api.mexc.com/api/v3/klines?symbol={s}&interval={i}&limit={l}"
 try:r=requests.get(u,timeout=10);r.raise_for_status();j=r.json()
 df=pd.DataFrame(j,columns=["open_time","open","high","low","close","volume","close_time","qv","trades","tbv","tbq","x"])
 df["open_time"]=pd.to_datetime(df["open_time"],unit="ms")
 df["close_time"]=pd.to_datetime(df["close_time"],unit="ms")
 df[["open","high","low","close","volume"]]=df[["open","high","low","close","volume"]].astype(float)
 return df
 except Exception as e:print(f"❌ خطا در دریافت داده برای {s}: {e}");return pd.DataFrame()
""",
    "TradingApp/utils/strategy.py": """import talib
def generate_signal(df,ai="bullish",tf="bullish"):
 ha=(df["open"]+df["high"]+df["low"]+df["close"])/4
 ma10=talib.SMA(ha,10);up,_,lo=talib.BBANDS(df["close"],20)
 pb=(df["close"]-lo)/(up-lo)
 m,mx,_=talib.MACD(df["close"])
 mu=m.iloc[-2]<mx.iloc[-2] and m.iloc[-1]>mx.iloc[-1]
 md=m.iloc[-2]>mx.iloc[-2] and m.iloc[-1]<mx.iloc[-1]
 k,d=talib.STOCHRSI(df["close"]);su=k.iloc[-2]<20 and k.iloc[-1]>d.iloc[-1];sd=k.iloc[-2]>80 and k.iloc[-1]<d.iloc[-1]
 e=talib.CDLENGULFING(df["open"],df["high"],df["low"],df["close"])
 bull=e.iloc[-1]>0;bear=e.iloc[-1]<0
 vol=df["volume"].iloc[-1]>df["volume"].rolling(20).mean().iloc[-1]
 if ma10.iloc[-1]<ha.iloc[-1] and pb.iloc[-1]>pb.iloc[-2] and mu and su and bull and vol and ai=="bullish" and tf=="bullish":
  return {"type":"LONG","stop":round(df["low"].iloc[-1]*0.995,2)}
 if ma10.iloc[-1]>ha.iloc[-1] and pb.iloc[-1]<pb.iloc[-2] and md and sd and bear and vol and ai=="bearish" and tf=="bearish":
  return {"type":"SHORT","stop":round(df["high"].iloc[-1]*1.005,2)}
 return None
""",
    "TradingApp/utils/notify.py": """import os,smtplib,requests
def send_email(msg):
 u,p,t=os.getenv("EMAIL_USER"),os.getenv("EMAIL_PASS"),os.getenv("EMAIL_TO")
 if not u or not p or not t:return print("❌ ایمیل تنظیم نشده")
 try:s=smtplib.SMTP("smtp.mail.yahoo.com",587);s.starttls();s.login(u,p);s.sendmail(u,t,msg);s.quit();print("✅ ایمیل ارسال شد.")
 except Exception as e:print(f"❌ ایمیل: {e}")
def send_telegram(msg):
 tk,cid=os.getenv("TELEGRAM_BOT_TOKEN"),os.getenv("TELEGRAM_CHAT_ID")
 if not tk or not cid:return print("❌ تلگرام تنظیم نشده")
 try:r=requests.post(f"https://api.telegram.org/bot{tk}/sendMessage",data={"chat_id":cid,"text":msg},timeout=10);r.raise_for_status();print("✅ پیام تلگرام ارسال شد.")
 except Exception as e:print(f"❌ تلگرام: {e}")
""",
    "TradingApp/scripts/signal_bot.py": """from TradingApp.utils.data import get_mexc_klines
from TradingApp.utils.strategy import generate_signal
from TradingApp.utils.notify import send_email,send_telegram
symbols=["BTCUSDT","ETHUSDT","XRPUSDT","LTCUSDT","DOGEUSDT","SHIBUSDT","TRXUSDT","ADAUSDT","DOTUSDT","BNBUSDT"]
for s in symbols:
 print(f"📡 دریافت داده برای {s}...")
 df=get_mexc_klines(s)
 if df.empty:print("⚠️ دیتافریم خالی است.");continue
 sig=generate_signal(df,ai="bullish",tf="bullish")
 if sig:
  msg=f"📈 سیگنال {sig['type']} برای {s}\nحد ضرر: {sig['stop']}"
  send_email(msg);send_telegram(msg)
 else:print(f"⏳ سیگنالی برای {s} یافت نشد.")
""",
    "TradingApp/scripts/test_notify.py": """from TradingApp.utils.notify import send_email,send_telegram
send_email("📧 تست ایمیل از smartsignalbot\nاین یک پیام تستی است.")
send_telegram("📲 تست تلگرام: این یک پیام تستی است.")
"""
}

def setup():
 for f in folders: os.makedirs(os.path.join(base,f),exist_ok=True)
 for path,content in files.items():
  full=os.path.join(base,path)
  with open(full,"w",encoding="utf-8") as f: f.write(content)
 print("✅ همه فایل‌ها ساخته یا بازنویسی شدند.")

setup()