import os,smtplib,requests
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
