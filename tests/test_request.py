import requests
from app import app
resp = requests.post(
    "http://127.0.0.1:5000/webhook/mattermost",
    data={
        "token": "dummy_token",
        "text": "bắt đầu workflow"
    }
)
print(resp.status_code, resp.text)
