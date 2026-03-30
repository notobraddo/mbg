import json
from openai import OpenAI
from config import AI_KEY, AI_MODEL

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=AI_KEY
)

def load_memory():
    try:
        return json.load(open("data/memory.json"))
    except:
        return {}

def memory_filter(signal, memory):
    key = signal["signal"]

    if key in memory:
        if memory[key]["winrate"] < 0.4:
            return False

    return True


async def ai_validate(signal):
    res = client.chat.completions.create(
        model=AI_MODEL,
        messages=[{"role":"user","content":str(signal)}]
    )

    return res.choices[0].message.content
