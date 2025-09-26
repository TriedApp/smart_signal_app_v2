code = '''
import requests, pandas as pd, numpy as np

excluded = ["IMXUSDT","FLOWUSDT","CVCUSDT","DENTUSDT","TOMOUSDT","INJUSDT","GMXUSDT","LDOUSDT","RNDRUSDT","DYDXUSDT","ARBUSDT","OPUSDT"]
nobitex_symbols = ["BTCUSDT","ETHUSDT","XRPUSDT","DOGEUSDT","TRXUSDT","SOLUSDT","ADAUSDT","DOTUSDT","AVAXUSDT","SHIBUSDT","UNIUSDT","LINKUSDT","MATICUSDT","LTCUSDT","BCHUSDT","XLMUSDT","EOSUSDT","ATOMUSDT","NEARUSDT","FTMUSDT","SANDUSDT","APEUSDT","AAVEUSDT","GRTUSDT","CHZUSDT","ETCUSDT","RUNEUSDT","CRVUSDT","1INCHUSDT","COMPUSDT","SNXUSDT"]
valid_symbols = [s for s in nobitex_symbols if s not in excluded]

def fetch_ohlcv_mexc(symbol, interval="15m", limit=300):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        data = requests.get(url).json()
        if not isinstance(data, list) or len(data) == 0 or len(data[0]) < 6:
            print(f"⚠️ داده ناقص برای {symbol}")
            return None
        df = pd.DataFrame(data, columns=["timestamp","open","high","low","close","volume","close_time","quote_volume"])
        return df[["open","high","low","close","volume"]].astype(float)
    except Exception as e:
        print(f"❌ خطا در دریافت داده برای {symbol}: {e}")
        return None

def sma(s,l): return s.rolling(l).mean()
def bollinger(s,l=20,d=2): m,std = sma(s,l), s.rolling(l).std(); return m+d*std, m-d*std, (s-(m-d*std))/(2*d*std)
def macd(s,f=12,sl=26,sg=9): ef,es = s.ewm(span=f,adjust=False).mean(), s.ewm(span=sl,adjust=False).mean(); m = ef-es; sig = m.ewm(span=sg,adjust=False).mean(); return m,sig,m-sig
def stoch_rsi(df,l=14): mn, mx = df['low'].rolling(l).min(), df['high'].rolling(l).max(); return 100*(df['close']-mn)/(mx-mn)
def heikin(df): h = df.copy(); h['ha_close'] = (df['open']+df['high']+df['low']+df['close'])/4; ho = [(df['open'][0]+df['close'][0])/2]; [ho.append((ho[i-1]+h['ha_close'][i-1])/2) for i in range(1,len(df))]; h['ha_open'] = ho; h['ha_high'] = df[['high','low','open','close']].max(axis=1); h['ha_low'] = df[['high','low','open','close']].min(axis=1); return h
def engulf(prev,curr): return curr['close']>curr['open'] and prev['close']<prev['open'] and curr['close']>prev['open'] and curr['open']<prev['close']
def take_profit(row,tol=0.001): return any(not pd.isna(row[m]) and abs(row['close']-row[m])/row[m]<tol for m in ['sma10','sma50','sma200'])

def run_strategy(df):
    ha = heikin(df)
    df[['ha_open','ha_close','ha_high','ha_low']] = ha[['ha_open','ha_close','ha_high','ha_low']]
    df['sma10'],df['sma50'],df['sma200'] = sma(df['close'],10),sma(df['close'],50),sma(df['close'],200)
    df['bb_u'],df['bb_l'],df['bb_p'] = bollinger(df['close'])
    df['macd'],df['macd_sig'],df['macd_hist'] = macd(df['close'])
    df['stoch'] = stoch_rsi(df)

    signals = []
    for i in range(1,len(df)):
        r,p = df.iloc[i],df.iloc[i-1]
        cond = all([
            r['low'] > r['sma10'],
            p['bb_p'] < 0.2 and r['bb_p'] > 0.2,
            p['macd'] < p['macd_sig'] and r['macd'] > r['macd_sig'],
            p['stoch'] < 20 and r['stoch'] > 20,
            engulf(p,r),
            r['ha_close'] > r['ha_open'] and r['ha_low'] > r['ha_open']*0.995
        ])
        if cond: signals.append((df.index[i],'LONG',r['close'],r['low']*0.995,take_profit(r)))

    r,p = df.iloc[-1],df.iloc[-2]
    print("\\n🔍 بررسی کندل آخر:")
    print(f"SMA10: {r['sma10']:.2f}, Low: {r['low']:.2f}")
    print(f"BB% Prev: {p['bb_p']:.2f}, BB% Now: {r['bb_p']:.2f}")
    print(f"MACD Prev: {p['macd']:.2f}, Signal Prev: {p['macd_sig']:.2f}")
    print(f"MACD Now: {r['macd']:.2f}, Signal Now: {r['macd_sig']:.2f}")
    print(f"Stoch RSI Prev: {p['stoch']:.2f}, Now: {r['stoch']:.2f}")
    print(f"HA Open: {r['ha_open']:.2f}, HA Close: {r['ha_close']:.2f}, HA Low: {r['ha_low']:.2f}")
    print(f"Engulfing: {engulf(p,r)}")

    return signals

def run_all():
    print("🚀 شروع بررسی نمادهای نوبیتکس...")
    for s in valid_symbols:
        df = fetch_ohlcv_mexc(s)
        if df is None or len(df) < 50:
            print(f"⚠️ داده کافی برای {s} موجود نیست."); continue
        sigs = run_strategy(df)
        if not sigs: print(f"❌ هیچ سیگنالی برای {s} صادر نشد.")
        for sig in sigs:
            print(f"✅ سیگنال برای {s} در {sig[0]} → قیمت: {sig[2]:.2f} | SL: {sig[3]:.2f} | TP: {'✅' if sig[4] else '❌'}")

if __name__ == "__main__": run_all()
'''

with open("signal_dispatcher.py", "w", encoding="utf-8") as f:
    f.write(code.strip())

print("✅ فایل signal_dispatcher.py با موفقیت جایگزین شد.")