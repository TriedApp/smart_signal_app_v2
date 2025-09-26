import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

# داده‌ی کندل‌ها (نمونه‌ای که فرستادی)
data = [
    {"close":"117541","created_at":1758211200000,"high":"117746","low":"117491","market":"BTCUSDT","open":"117589","value":"2203920.64534683","volume":"18.7317522"},
    {"close":"117548","created_at":1758214800000,"high":"117750","low":"117418","market":"BTCUSDT","open":"117540","value":"1519164.8399777","volume":"12.92126423"},
    {"close":"117811","created_at":1758218400000,"high":"117876","low":"117500","market":"BTCUSDT","open":"117548","value":"2495698.16922195","volume":"21.19710298"},
    {"close":"117445","created_at":1758222000000,"high":"117811","low":"117203","market":"BTCUSDT","open":"117811","value":"1968870.66537078","volume":"16.7611501"},
    {"close":"117509","created_at":1758225600000,"high":"117614","low":"117383","market":"BTCUSDT","open":"117445","value":"1135718.70222109","volume":"9.66626406"},
    {"close":"117306","created_at":1758229200000,"high":"117509","low":"117303","market":"BTCUSDT","open":"117509","value":"741451.22263222","volume":"6.3173729"},
    {"close":"117052","created_at":1758232800000,"high":"117302","low":"117050","market":"BTCUSDT","open":"117294","value":"417923.26493212","volume":"3.56718812"},
    {"close":"117094","created_at":1758236400000,"high":"117143","low":"116650","market":"BTCUSDT","open":"117053","value":"1127401.88150426","volume":"9.65063492"},
    {"close":"117398","created_at":1758240000000,"high":"117399","low":"117071","market":"BTCUSDT","open":"117094","value":"837205.31661975","volume":"7.13752602"},
    {"close":"117232","created_at":1758243600000,"high":"117427","low":"117162","market":"BTCUSDT","open":"117399","value":"314361.49940692","volume":"2.6801042"},
    {"close":"117097","created_at":1758247200000,"high":"117256","low":"117047","market":"BTCUSDT","open":"117218","value":"470713.76496465","volume":"4.01866059"},
    {"close":"116938","created_at":1758250800000,"high":"117257","low":"116859","market":"BTCUSDT","open":"117097","value":"976280.002779","volume":"8.33949477"},
    {"close":"116968","created_at":1758254400000,"high":"117058","low":"116692","market":"BTCUSDT","open":"116939","value":"1521082.04430615","volume":"13.0154356"}
]

# تبدیل به DataFrame
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['created_at'], unit='ms')
df['close'] = df['close'].astype(float)

# محاسبه‌ی EMA و RSI
df['EMA_20'] = EMAIndicator(close=df['close'], window=5).ema_indicator()
df['EMA_50'] = EMAIndicator(close=df['close'], window=10).ema_indicator()
df['RSI'] = RSIIndicator(close=df['close'], window=5).rsi()

# صدور سیگنال
def generate_signal(row):
    if row['EMA_20'] > row['EMA_50'] and row['RSI'] > 50:
        return 'BUY'
    elif row['EMA_20'] < row['EMA_50'] and row['RSI'] < 50:
        return 'SELL'
    else:
        return 'HOLD'

df['signal'] = df.apply(generate_signal, axis=1)

# نمایش آخرین سیگنال
latest = df.iloc[-1]
print(f"📊 آخرین سیگنال برای BTCUSDT:")
print(f"EMA20: {latest['EMA_20']:.2f}, EMA50: {latest['EMA_50']:.2f}, RSI: {latest['RSI']:.2f}")
print(f"✅ سیگنال نهایی: {latest['signal']}")