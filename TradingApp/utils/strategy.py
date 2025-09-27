import pandas as pd

def sma(s, l): return s.rolling(l).mean()
def bollinger(s, l=20, d=2): m = sma(s, l); std = s.rolling(l).std(); u = m + d*std; l = m - d*std; b = (s - l) / (u - l); return u, l, b
def macd(s, f=12, sl=26, sig=9): ef, es = s.ewm(span=f).mean(), s.ewm(span=sl).mean(); m = ef - es; sg = m.ewm(span=sig).mean(); h = m - sg; return m, sg, h
def stochrsi(df, l=14): lo, hi = df['low'].rolling(l).min(), df['high'].rolling(l).max(); return 100 * (df['close'] - lo) / (hi - lo)
def heikin(df): ha = df.copy(); ha['ha_close'] = df[['open','high','low','close']].mean(axis=1); ho = [(df['open'][0]+df['close'][0])/2]; [ho.append((ho[i-1]+ha['ha_close'][i-1])/2) for i in range(1,len(df))]; ha['ha_open'] = ho; ha['ha_high'] = df[['high','low','open','close']].max(axis=1); ha['ha_low'] = df[['high','low','open','close']].min(axis=1); return ha
def engulf_up(p,c): return c['close']>c['open'] and p['close']<p['open'] and c['close']>p['open'] and c['open']<p['close']
def engulf_down(p,c): return c['close']<c['open'] and p['close']>p['open'] and c['close']<p['open'] and c['open']>p['close']
def ha_pos(r): return 'above' if r['ha_low']>r['sma10'] else 'below' if r['ha_high']<r['sma10'] else 'inside'
def takeprofit(r,tol=0.001): return any(abs(r['ha_close']-r[m])/r[m]<tol for m in ['sma10','sma50','sma200'] if pd.notna(r[m]))
def vol_ok(df,i): return True if i<10 else df['volume'].iloc[i]>df['volume'].iloc[i-10:i].mean()
def ai_ok(r): return sum([r['macd']>r['macd_signal'], r['close']>r['sma50'], r['sma10']>r['sma50']])>=2

def run_strategy(df, df_htf=None, debug=False):
    ha = heikin(df)
    for k in ['ha_open','ha_close','ha_high','ha_low']: df[k] = ha[k]
    df['sma10'], df['sma50'], df['sma200'] = sma(df['close'],10), sma(df['close'],50), sma(df['close'],200)
    df['bb_upper'], df['bb_lower'], df['bb_percent_b'] = bollinger(df['close'])
    df['macd'], df['macd_signal'], df['macd_hist'] = macd(df['close'])
    df['stoch_rsi'] = stochrsi(df)
    signals = []

    for i in range(1,len(df)):
        r, p = df.iloc[i], df.iloc[i-1]
        htf_ok = True
        if df_htf is not None:
            t = df_htf.index[df_htf.index <= df.index[i]]
            if len(t): htf_ok = df_htf.loc[t[-1]]['ha_close'] > df_htf.loc[t[-1]]['ha_open']

        long = {
            "MA10": ha_pos(r)=='above',
            "Bollinger": p['bb_percent_b']<0.2 and r['bb_percent_b']>0.2,
            "MACD": p['macd']<p['macd_signal'] and r['macd']>r['macd_signal'],
            "StochRSI": p['stoch_rsi']<20 and r['stoch_rsi']>20,
            "Engulf": engulf_up(p,r),
            "Volume": vol_ok(df,i),
            "AI": ai_ok(r),
            "HTF": htf_ok
        }

        short = {
            "MA10": ha_pos(r)=='below',
            "Bollinger": p['bb_percent_b']>0.8 and r['bb_percent_b']<0.8,
            "MACD": p['macd']>p['macd_signal'] and r['macd']<r['macd_signal'],
            "StochRSI": p['stoch_rsi']>80 and r['stoch_rsi']<80,
            "Engulf": engulf_down(p,r),
            "Volume": vol_ok(df,i),
            "AI": not ai_ok(r),
            "HTF": not htf_ok
        }

        if debug:
            print(f"\n🟢 LONG @ {df.index[i]}"); [print(f"📌 {k}: {v}") for k,v in long.items()]
            print(f"\n🔴 SHORT @ {df.index[i]}"); [print(f"📌 {k}: {v}") for k,v in short.items()]

        if all(long.values()):
            signals.append((df.index[i],'LONG',r['close'],r['low']*0.995,takeprofit(r)))
        if all(short.values()):
            signals.append((df.index[i],'SHORT',r['close'],r['high']*1.005,takeprofit(r)))

    return signals