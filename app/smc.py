import numpy as np

# =========================
# SWING STRUCTURE
# =========================
def swings(df, n=3):
    highs, lows = [], []

    for i in range(n, len(df)-n):
        if df['high'].iloc[i] == max(df['high'].iloc[i-n:i+n]):
            highs.append((i, df['high'].iloc[i]))

        if df['low'].iloc[i] == min(df['low'].iloc[i-n:i+n]):
            lows.append((i, df['low'].iloc[i]))

    return highs, lows


# =========================
# BOS + CHOCH
# =========================
def structure(df):
    highs, lows = swings(df)

    bos = None
    choch = None

    if len(highs) > 2 and len(lows) > 2:
        if highs[-1][1] > highs[-2][1]:
            bos = "BULLISH"
        if lows[-1][1] < lows[-2][1]:
            bos = "BEARISH"

        if bos == "BULLISH" and lows[-1][1] < lows[-2][1]:
            choch = "BEARISH"
        if bos == "BEARISH" and highs[-1][1] > highs[-2][1]:
            choch = "BULLISH"

    return bos, choch


# =========================
# LIQUIDITY POOL (EQH/EQL)
# =========================
def liquidity_pool(df, tolerance=0.001):
    pools = []

    for i in range(len(df)-5):
        h1 = df['high'].iloc[i]
        h2 = df['high'].iloc[i+2]

        if abs(h1 - h2)/h1 < tolerance:
            pools.append(("EQH", h1))

        l1 = df['low'].iloc[i]
        l2 = df['low'].iloc[i+2]

        if abs(l1 - l2)/l1 < tolerance:
            pools.append(("EQL", l1))

    return pools


# =========================
# FVG (FAIR VALUE GAP)
# =========================
def fvg(df):
    gaps = []

    for i in range(2, len(df)):
        prev = df.iloc[i-2]
        curr = df.iloc[i]

        # bullish gap
        if prev['high'] < curr['low']:
            gaps.append(("bullish", prev['high'], curr['low']))

        # bearish gap
        if prev['low'] > curr['high']:
            gaps.append(("bearish", curr['high'], prev['low']))

    return gaps


# =========================
# LIQUIDITY SWEEP
# =========================
def sweep(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    if last['high'] > prev['high'] and last['close'] < prev['high']:
        return "SWEEP_HIGH"

    if last['low'] < prev['low'] and last['close'] > prev['low']:
        return "SWEEP_LOW"

    return None


# =========================
# SNIPER ENTRY LOGIC
# =========================
def sniper(df):
    bos, choch = structure(df)
    gaps = fvg(df)
    sw = sweep(df)

    if bos == "BULLISH" and sw == "SWEEP_LOW":
        return "BUY"

    if bos == "BEARISH" and sw == "SWEEP_HIGH":
        return "SELL"

    return None