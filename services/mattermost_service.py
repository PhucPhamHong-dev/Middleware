import requests
from flask import current_app

def send_message(text: str):
    url = current_app.config["MATTERMOST_WEBHOOK_URL"]
    payload = {"text": text}
    requests.post(url, json=payload, timeout=5)
