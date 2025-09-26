import talib
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
