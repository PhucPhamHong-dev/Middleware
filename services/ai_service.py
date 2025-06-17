import requests
from flask import current_app

def analyze_text(text: str) -> dict:
    url = current_app.config["AI_ENGINE_URL"]
    headers = {"Authorization": f"Bearer {current_app.config['AI_ENGINE_KEY']}"}
    payload = {"text": text}
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()
