# tests/test_mattermost_handler.py
import pytest
from fastapi.testclient import TestClient
from mattermost_handler import app, analyze_text

client = TestClient(app)

VALID_PAYLOAD = {
    "token": "12345",
    "team_id": "T123",
    "channel_id": "C123",
    "user_name": "teamlan",
    "text": "   thử nghiệm xử lý   ",
    "command": "/test"
}

INVALID_TOKEN_PAYLOAD = VALID_PAYLOAD.copy()
INVALID_TOKEN_PAYLOAD["token"] = "WRONG_TOKEN"

def test_analyze_text_mock():
    sample = "hello world"
    result = analyze_text(sample)
    assert "Intent:" in result
    assert "Original: hello world" in result

def test_handle_valid_payload():
    resp = client.post("/mattermost/webhook", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    data = resp.json()
    assert data["response_type"] == "in_channel"
    assert "Intent:" in data["text"]
    assert "Original: thử nghiệm xử lý" in data["text"]

def test_handle_invalid_token():
    resp = client.post("/mattermost/webhook", json=INVALID_TOKEN_PAYLOAD)
    assert resp.status_code == 403
    assert resp.json()["detail"] == "Invalid token"

def test_missing_field():
    payload = VALID_PAYLOAD.copy()
    payload.pop("text")
    resp = client.post("/mattermost/webhook", json=payload)
    assert resp.status_code == 422
