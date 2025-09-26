import talib
import pandas as pd

def heikin_ashi(df):
    ha_df = pd.DataFrame(index=df.index)
    ha_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    ha_df['open'] = (df['open'].shift(1) + df['close'].shift(1)) / 2
    ha_df['high'] = df[['high', 'open', 'close']].max(axis=1)
    ha_df['low'] = df[['low', 'open', 'close']].min(axis=1)
    return ha_df

def generate_signal(df_dict, ai_trend="bullish", tf1h_trend="bullish"):
    df_1h = df_dict.get("1hour")
    if df_1h is None or df_1h.empty:
        return None

    ha = heikin_ashi(df_1h)
    ma10 = talib.SMA(ha['close'], timeperiod=10)
    up, mid, lo = talib.BBANDS(df_1h['close'], timeperiod=20)
    pb = (df_1h['close'] - lo) / (up - lo)

    macd, macd_signal, _ = talib.MACD(df_1h['close'])
    macd_cross_up = macd.iloc[-2] < macd_signal.iloc[-2] and macd.iloc[-1] > macd_signal.iloc[-1]
    macd_cross_down = macd.iloc[-2] > macd_signal.iloc[-2] and macd.iloc[-1] < macd_signal.iloc[-1]

    k, d = talib.STOCHRSI(df_1h['close'])
    stoch_up = k.iloc[-2] < 20 and k.iloc[-1] > d.iloc[-1]
    stoch_down = k.iloc[-2] > 80 and k.iloc[-1] < d.iloc[-1]

    engulf = talib.CDLENGULFING(df_1h['open'], df_1h['high'], df_1h['low'], df_1h['close'])
    bullish_engulf = engulf.iloc[-1] > 0
    bearish_engulf = engulf.iloc[-1] < 0

    volume_ok = df_1h['volume'].iloc[-1] > df_1h['volume'].rolling(20).mean().iloc[-1]

    conditions_long = [
        ma10.iloc[-1] < ha['close'].iloc[-1],
        pb.iloc[-1] > pb.iloc[-2],
        macd_cross_up,
        stoch_up,
        bullish_engulf,
        volume_ok,
        ai_trend == "bullish",
        tf1h_trend == "bullish"
    ]

    conditions_short = [
        ma10.iloc[-1] > ha['close'].iloc[-1],
        pb.iloc[-1] < pb.iloc[-2],
        macd_cross_down,
        stoch_down,
        bearish_engulf,
        volume_ok,
        ai_trend == "bearish",
        tf1h_trend == "bearish"
    ]

    strength_long = sum(conditions_long)
    strength_short = sum(conditions_short)

    if strength_long >= 6:
        stop = round(df_1h['low'].iloc[-1] * 0.995, 4)
        take_profit = "MA10/50/200 نزدیک شد"
        return {
            "type": "LONG",
            "strength": "strong" if strength_long == 8 else "moderate",
            "stop": stop,
            "take_profit": take_profit
        }

    if strength_short >= 6:
        stop = round(df_1h['high'].iloc[-1] * 1.005, 4)
        take_profit = "MA10/50/200 نزدیک شد"
        return {
            "type": "SHORT",
            "strength": "strong" if strength_short == 8 else "moderate",
            "stop": stop,
            "take_profit": take_profit
        }

    return None