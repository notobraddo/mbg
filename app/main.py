import asyncio
import aiohttp

from data import get_symbols, get_candles
from indicators import to_df, rsi
from strategy import analyze, score
from ai import memory_filter, ai_validate, load_memory
from telegram import send
from storage import save

TIMEFRAMES = ["1d","4h","1h","15m"]

async def run():
    symbols = (await get_symbols())[:30]
    memory = load_memory()

    async with aiohttp.ClientSession() as session:
        results = []

        for symbol in symbols:
            confirm = 0
            last_data = None
            final_signal = None
            smc_data = None

            for tf in TIMEFRAMES:
                data = await get_candles(session, symbol, tf)
                if not data or len(data) < 50:
                    continue

                df = rsi(to_df(data))
                sig, last, smc = analyze(df)

                if sig:
                    confirm += 1
                    final_signal = sig
                    last_data = last
                    smc_data = smc

            if confirm >= 3:
                s = score(final_signal, smc_data)

                signal = {
                    "symbol": symbol,
                    "signal": final_signal,
                    "score": s
                }

                if not memory_filter(signal, memory):
                    continue

                results.append((signal, smc_data))

        results = sorted(results, key=lambda x: x[0]["score"], reverse=True)[:20]

        for r, smc in results:
            ai = await ai_validate(r)

            msg = f"""
{r['symbol']} {r['signal']}
Score: {r['score']}

BOS: {smc['bos']}
Sweep: {smc['sweep']}
FVG: {smc['fvg']}
Liquidity: {smc['pools']}

AI:
{ai}
"""

            send(msg)
            save(r)


async def loop():
    while True:
        try:
            await run()
        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(900)


if __name__ == "__main__":
    asyncio.run(loop())
