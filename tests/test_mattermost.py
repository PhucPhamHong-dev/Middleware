import pytest
from app import app
import controllers.mattermost_controller as mm_controller

@pytest.fixture
def client():
    # đảm bảo token khớp
    app.config["MATTERMOST_TOKEN"] = "dummy_token"
    return app.test_client()

def test_webhook_flow(monkeypatch, client):
    # 1) Stub AI ngay trong controller
    monkeypatch.setattr(
        mm_controller,
        "analyze_text",
        lambda text: {
            "intent": "initiate_workflow",
            "workflow_name": "TPV-Test",
            "tasks": [{"title": "T1", "description": ""}]
        }
    )

    # 2) Stub send_message ngay trong controller
    sent = {}
    monkeypatch.setattr(
        mm_controller,
        "send_message",
        lambda text: sent.update({"text": text})
    )

    # 3) Gọi thử webhook
    rv = client.post(
        "/webhook/mattermost",
        data={"token": "dummy_token", "text": "run test"}
    )

    # 4) Assert
    assert rv.status_code == 200
    assert "TPV-Test" in sent["text"]
