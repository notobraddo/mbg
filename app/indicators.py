import pandas as pd

def to_df(data):
    df = pd.DataFrame(data)
    df.columns = ["time","open","high","low","close","volume"]
    return df

def rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rs = gain.rolling(period).mean() / loss.rolling(period).mean()
    df['rsi'] = 100 - (100/(1+rs))
    return df