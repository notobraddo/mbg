import aiohttp
import asyncio
from app.config import API_URL

SEM = asyncio.Semaphore(5)

async def fetch(session, payload):
    async with SEM:
        async with session.post(API_URL, json=payload) as res:
            return await res.json()

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