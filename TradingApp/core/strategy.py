def is_bullish_engulfing(prev, row):
    return prev['close'] < prev['open'] and row['close'] > row['open'] and row['close'] > prev['open'] and row['open'] < prev['close']

def is_bearish_engulfing(prev, row):
    return prev['close'] > prev['open'] and row['close'] < row['open'] and row['close'] < prev['open'] and row['open'] > prev['close']

def check_take_profit(row):
    return row['close'] > row.get('sma50', row['close'])

def run_strategy(df):
    signals = []
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        row = df.iloc[i]

        long_cond = all([
            row['low'] > row['sma10'],
            prev['bb_percent_b'] < 0.2 and row['bb_percent_b'] > 0.2,
            prev['macd'] < prev['macd_signal'] and row['macd'] > row['macd_signal'],
            prev['stoch_rsi'] < 20 and row['stoch_rsi'] > 20,
            is_bullish_engulfing(prev, row)
        ])
        if long_cond:
            sl = row['low'] * 0.995
            tp = check_take_profit(row)
            signals.append((df.index[i], 'LONG', row['close'], sl, tp))

        short_cond = all([
            row['high'] < row['sma10'],
            prev['bb_percent_b'] > 0.8 and row['bb_percent_b'] < 0.8,
            prev['macd'] > prev['macd_signal'] and row['macd'] < row['macd_signal'],
            prev['stoch_rsi'] > 80 and row['stoch_rsi'] < 80,
            is_bearish_engulfing(prev, row)
        ])
        if short_cond:
            sl = row['high'] * 1.005
            tp = check_take_profit(row)
            signals.append((df.index[i], 'SHORT', row['close'], sl, tp))

    return signals

def run_strategies():
    import pandas as pd

    def get_mexc_data():
        return pd.DataFrame([{
            'low': 100, 'high': 110, 'close': 105, 'open': 102,
            'sma10': 98, 'sma50': 104,
            'bb_percent_b': 0.25,
            'macd': 1.2, 'macd_signal': 1.1,
            'stoch_rsi': 25
        }, {
            'low': 102, 'high': 112, 'close': 106, 'open': 101,
            'sma10': 99, 'sma50': 105,
            'bb_percent_b': 0.3,
            'macd': 1.3, 'macd_signal': 1.2,
            'stoch_rsi': 30
        }])

    def get_cg_data():
        return get_mexc_data()

    df_mexc = get_mexc_data()
    df_cg = get_cg_data()
    return run_strategy(df_mexc) + run_strategy(df_cg)
