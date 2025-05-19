
import requests, os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def chat(query: str) -> str:
    resp = requests.post(f"{BACKEND_URL}/chat/", json={ "query": query }, timeout=60)
    resp.raise_for_status()
    return resp.json().get("answer", "")
