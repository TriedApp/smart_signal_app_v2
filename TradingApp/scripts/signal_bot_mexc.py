import os, smtplib, aiohttp, asyncio, pandas as pd, numpy as np, schedule, time
from email.mime.text import MIMEText

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "DOGEUSDT", "SHIBUSDT", "TRXUSDT", "ADAUSDT", "DOTUSDT", "BNBUSDT",
    "SOLUSDT", "AVAXUSDT", "UNIUSDT", "LINKUSDT", "XLMUSDT", "ATOMUSDT", "EOSUSDT", "DAIUSDT", "USDCUSDT", "MATICUSDT",
    "AAVEUSDT", "AXSUSDT", "SANDUSDT", "CHZUSDT", "FTMUSDT", "NEARUSDT", "GALAUSDT", "RAYUSDT", "CAKEUSDT", "CRVUSDT",
    "1INCHUSDT", "ENJUSDT", "BCHUSDT", "ETCUSDT", "XMRUSDT", "ZECUSDT", "SNXUSDT", "COMPUSDT", "YFIUSDT", "ALGOUSDT",
    "TOMOUSDT", "KSMUSDT", "KNCUSDT", "RENUSDT", "BATUSDT", "SUSHIUSDT", "STORJUSDT", "CELRUSDT", "ANKRUSDT", "CVCUSDT",
    "BALUSDT", "GMTUSDT", "LRCUSDT", "DYDXUSDT", "GMXUSDT", "OPUSDT", "ARBUSDT", "INJUSDT", "PEPEUSDT", "FLOKIUSDT",
    "ORDIUSDT", "WLDUSDT", "TUSDUSDT", "PYTHUSDT", "BONKUSDT", "TIAUSDT", "JUPUSDT", "GRTUSDT", "RNDRUSDT", "LPTUSDT",
    "MINAUSDT", "BLURUSDT", "ICPUSDT", "APTUSDT", "SUIUSDT", "C98USDT", "XVSUSDT", "RUNEUSDT", "DODOUSDT", "HOOKUSDT",
    "SSVUSDT", "IDUSDT", "LDOUSDT", "FETUSDT", "AGIXUSDT", "OCEANUSDT", "BANDUSDT", "QNTUSDT", "STMXUSDT", "XNOUSDT",
    "NMRUSDT", "NKNUSDT", "CTSIUSDT", "SKLUSDT", "VETUSDT", "VTHOUSDT", "COTIUSDT", "MASKUSDT", "HIGHUSDT", "SPELLUSDT",
    "SXPUSDT", "DENTUSDT"
]
def sma(s,l): return s.rolling(l).mean()
def bollinger(s,l=20,d=2): m,std=sma(s,l),s.rolling(l).std(); return m+d*std,m-d*std,(s-m+d*std)/(2*d*std)
def macd(s,f=12,sl=26,sig=9): ef=s.ewm(span=f).mean(); es=s.ewm(span=sl).mean(); m=ef-es; ms=m.ewm(span=sig).mean(); return m,ms,m-ms
def stoch_rsi(df,l=14): lo=df['low'].rolling(l).min(); hi=df['high'].rolling(l).max(); return 100*(df['close']-lo)/(hi-lo)
def heikin(df):
    ha = df.copy()
    ha['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ho = [(df['open'].iloc[0] + df['close'].iloc[0]) / 2]
    for i in range(1, len(df)):
        ho.append((ho[i - 1] + ha['ha_close'].iloc[i - 1]) / 2)
    ha['ha_open'] = ho
    ha['ha_high'] = df[['high', 'low', 'open', 'close']].max(axis=1)
    ha['ha_low'] = df[['high', 'low', 'open', 'close']].min(axis=1)
    return ha
def engulf(prev,curr): return curr['close']>curr['open'] and prev['close']<prev['open'] and curr['close']>prev['open'] and curr['open']<prev['close']
def ha_pos(r): return 'above' if r['ha_low']>r['sma10'] else 'below' if r['ha_high']<r['sma10'] else 'inside'
def take_profit(r,t=0.001): return any(abs(r['ha_close']-r[m])/r[m]<t for m in ['sma10','sma50','sma200'] if not pd.isna(r[m]))
def volume_ok(df,i): return i<10 or df['volume'].iloc[i]>df['volume'].iloc[i-10:i].mean()
def ai_trend(r): return sum([r['macd']>r['macd_signal'],r['close']>r['sma50'],r['sma10']>r['sma50']])>=2
def run_strategy(df):
    ha = heikin(df)
    df['ha_open'], df['ha_close'], df['ha_high'], df['ha_low'] = ha['ha_open'], ha['ha_close'], ha['ha_high'], ha['ha_low']
    df['sma10'], df['sma50'], df['sma200'] = sma(df['close'], 10), sma(df['close'], 50), sma(df['close'], 200)
    df['bb_upper'], df['bb_lower'], df['bb_percent_b'] = bollinger(df['close'])
    df['macd'], df['macd_signal'], df['macd_hist'] = macd(df['close'])
    df['stoch_rsi'] = stoch_rsi(df)

    signals = []
    for i in range(1, len(df)):
        r, pr = df.iloc[i], df.iloc[i - 1]
        pos = ha_pos(r)
        long = all([
            pos == 'above',
            pr['bb_percent_b'] < 0.2 and r['bb_percent_b'] > 0.2,
            pr['macd'] < pr['macd_signal'] and r['macd'] > r['macd_signal'],
            pr['stoch_rsi'] < 20 and r['stoch_rsi'] > 20,
            engulf(pr, r),
            volume_ok(df, i),
            ai_trend(r)
        ])
        short = all([
            pos == 'below',
            pr['bb_percent_b'] > 0.8 and r['bb_percent_b'] < 0.8,
            pr['macd'] > pr['macd_signal'] and r['macd'] < r['macd_signal'],
            pr['stoch_rsi'] > 80 and r['stoch_rsi'] < 80,
            engulf(pr, r),
            volume_ok(df, i),
            not ai_trend(r)
        ])
        if long: signals.append((df.index[i], 'LONG', r['close'], r['low'] * 0.995, take_profit(r)))
        if short: signals.append((df.index[i], 'SHORT', r['close'], r['high'] * 1.005, take_profit(r)))
    return signals
async def fetch_ohlcv_async(session, symbol, interval='30m', limit=100):
    url = f'https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    async with session.get(url) as resp:
        data = await resp.json()
        df = pd.DataFrame(data, columns=['time','open','high','low','close','volume','x','y','z','w','v','u'])
        df = df[['time','open','high','low','close','volume']].astype(float)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        return symbol, df

async def fetch_all_symbols():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_ohlcv_async(session, symbol) for symbol in SYMBOLS]
        return await asyncio.gather(*tasks)
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = os.environ['EMAIL_TO']
    with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

def send_telegram(text):
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})
def run_bot_async():
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fetch_all_symbols())

    all_signals = []
    for symbol, df in results:
        try:
            signals = run_strategy(df)
            for s in signals:
                line = f"{symbol} | {s[0]} | {s[1]} | قیمت: {s[2]:.4f} | SL: {s[3]:.4f} | TP نزدیک MA: {'✅' if s[4] else '❌'}"
                all_signals.append(line)
        except Exception as e:
            all_signals.append(f"{symbol}: ❌ خطا: {str(e)}")

    msg = "📊 سیگنال‌های جدید:\n\n" + "\n".join(all_signals) if all_signals else "⏸ هیچ سیگنالی یافت نشد."
    send_email("📈 گزارش سیگنال‌های MEXC", msg)
    send_telegram(msg)
    print("🚀 ربات شکار سیگنال MEXC (نسخه async) فعال شد...")

schedule.every(5).minutes.do(run_bot_async)

if __name__ == "__main__":
    print("🎯 ربات در حال اجراست (نسخه async)...")
    while True:
        schedule.run_pending()
        time.sleep(1)