import os, pandas as pd, requests, schedule, time, smtplib
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from strategy import run_strategy, heikin

def get_symbols():
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    data = requests.get(url).json()
    return [s['symbol'] for s in data['symbols'] if s['quoteAsset'] == 'USDT' and s['status'] == 'ENABLED']

def fetch_ohlcv(symbol, interval='15m', limit=100):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        data = requests.get(url, timeout=3).json()
        df = pd.DataFrame(data, columns=['time','open','high','low','close','volume','x','y','z','a','b'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        return df[['open','high','low','close','volume']].astype(float)
    except: return pd.DataFrame()

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'], msg['From'], msg['To'] = subject, os.environ['EMAIL_USER'], os.environ['EMAIL_TO']
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"
    requests.post(url, data={'chat_id': os.environ['TELEGRAM_CHAT_ID'], 'text': msg})

def notify(symbol, tf, signal):
    if isinstance(signal, str): msg = f"{symbol} | TF: {tf} | {signal}"
    else:
        t, typ, p, sl, tp = signal
        msg = f"{symbol} | TF: {tf} | {typ} @ {p:.4f} | SL: {sl:.4f} | TP: {'✅' if tp else '❌'}"
    send_email(f"سیگنال {symbol} - {tf}", msg)
    send_telegram(msg)

def check_symbol(symbol):
    results = []
    for tf in ['15m','30m','1h']:
        df = fetch_ohlcv(symbol, tf)
        htf = fetch_ohlcv(symbol, '1h')
        if df.empty or htf.empty: continue
        htf_ha = heikin(htf)
        htf['ha_open'], htf['ha_close'] = htf_ha['ha_open'], htf_ha['ha_close']
        for s in run_strategy(df, htf, debug=False): results.append((symbol, tf, s))
    return results

def run_bot():
    all_signals = []
    with ThreadPoolExecutor(max_workers=20) as ex:
        for res in ex.map(check_symbol, get_symbols()):
            for symbol, tf, sig in res:
                notify(symbol, tf, sig)
                all_signals.append(sig)
    if not all_signals:
        msg = "✅ ربات فعال است، هیچ سیگنالی یافت نشد."
        send_email("وضعیت ربات", msg)
        send_telegram(msg)

schedule.every(5).minutes.do(run_bot)
print("🚀 ربات شکار سیگنال MEXC فعال شد...")
while True:
    schedule.run_pending()
    time.sleep(1)