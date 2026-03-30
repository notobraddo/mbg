import os

API_URL = "https://api.hyperliquid.xyz/info"

TIMEFRAMES = ["1d","4h","1h","15m"]
TOP_N = 20
SCAN_INTERVAL = 900

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT = os.getenv("TG_CHAT")

AI_KEY = os.getenv("NVAPI_KEY")
AI_MODEL = "deepseek-ai/deepseek-v3.2"