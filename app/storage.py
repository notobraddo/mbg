import requests
from app.config import TG_TOKEN, TG_CHAT

def send(msg):
    if not TG_TOKEN:
        return

    requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        json={"chat_id": TG_CHAT, "text": msg}
    )