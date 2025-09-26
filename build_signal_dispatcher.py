code = '''
import requests, pandas as pd, numpy as np

def sma(s,l): return s.rolling(l).mean()
def bollinger(s,l=20,d=2): m,std = sma(s,l), s.rolling(l).std(); return m+d*std, m-d*std, (s-(m-d*std))/(2*d*std)
def macd(s,f=12,sl=26,sg=9): ef,es = s.ewm(span=f,adjust=False).mean(), s.ewm(span=sl,adjust=False).mean(); m = ef-es; sig = m.ewm(span=sg,adjust=False).mean(); return m,sig,m-sig
def stoch_rsi(df,l=14): mn, mx = df['low'].rolling(l).min(), df['high'].rolling(l).max(); return 100*(df['close']-mn)/(mx-mn)
def heikin(df): h = df.copy(); h['ha_close'] = (df['open']+df['high']+df['low']+df['close'])/4; ho = [(df['open'][0]+df['close'][0])/2]; [ho.append((ho[i-1]+h['ha_close'][i-1])/2) for i in range(1,len(df))]; h['ha_open'] = ho; h['ha_high'] = df[['high','low','open','close']].max(axis=1); h['ha_low'] = df[['high','low','open','close']].min(axis=1); return h
def engulf(prev,curr): return curr['close']>curr['open'] and prev['close']<prev['open'] and curr['close']>prev['open'] and curr['open']<prev['close']

def run_strategy(df):
    ha = heikin(df)
    df[['ha_open','ha_close','ha_high','ha_low']] = ha[['ha_open','ha_close','ha_high','ha_low']]
    df['sma10'] = sma(df['close'],10)
    df['bb_u'],df['bb_l'],df['bb_p'] = bollinger(df['close'])
    df['macd'],df['macd_sig'],df['macd_hist'] = macd(df['close'])
    df['stoch'] = stoch_rsi(df)

    signals = []
    for i in range(1,len(df)):
        r,p = df.iloc[i],df.iloc[i-1]
        cond = all([
            r['low'] > r['sma10'],
            p['bb_p'] < 0.3 and r['bb_p'] > 0.3,
            r['macd'] > r['macd_sig'],
            p['stoch'] < 30 and r['stoch'] > 30,
            engulf(p,r),
            r['ha_close'] > r['ha_open']
        ])
        if cond: signals.append((df.index[i],'LONG',r['close'],r['low']*0.995))

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
'''

with open("signal_dispatcher.py", "w", encoding="utf-8") as f:
    f.write(code.strip())

print("✅ فایل signal_dispatcher.py با موفقیت ساخته شد و آماده‌ی اجراست.")