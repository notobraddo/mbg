import aiohttp
import asyncio
from config import BASE_URL

SEM = asyncio.Semaphore(5)

async def fetch(session, payload):
    async with SEM:
        async with session.post(BASE_URL, json=payload) as res:
            
            if res.status != 200:
                text = await res.text()
                print("HTTP ERROR:", res.status, text)
                return None

            try:
                return await res.json()
            except:
                text = await res.text()
                print("NOT JSON RESPONSE:", text)
                return None

async def get_symbols():
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, {"type":"meta"})
        return [x["name"] for x in data["universe"]]

async def get_candles(session, symbol, tf):
    payload = {
        "type":"candleSnapshot",
        "req":{"coin":symbol,"interval":tf,"limit":150}
    }
    return await fetch(session, payload)
