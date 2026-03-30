from smc import structure, liquidity_pool, fvg, sweep, sniper

def analyze(df):
    bos, choch = structure(df)
    pools = liquidity_pool(df)
    gaps = fvg(df)
    sw = sweep(df)

    signal = sniper(df)

    last = df.iloc[-1]

    return signal, last, {
        "bos": bos,
        "choch": choch,
        "pools": pools[-2:],
        "fvg": gaps[-2:],
        "sweep": sw
    }


def score(signal, smc):
    s = 0

    if signal:
        s += 0.3

    if smc["bos"]:
        s += 0.2

    if smc["sweep"]:
        s += 0.2

    if smc["fvg"]:
        s += 0.15

    if smc["pools"]:
        s += 0.15

    return s
