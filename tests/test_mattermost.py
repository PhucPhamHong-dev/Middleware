import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

@patch("services.ai_service.analyze_text")
@patch("services.erp_service.create_project_with_tasks")
@patch("services.mattermost_service.send_message")
def test_initiate_workflow(mock_send, mock_create, mock_ai, client):
    mock_ai.return_value = {
        "intent": "initiate_workflow",
        "workflow_name": "Demo WF",
        "tasks": [{"title":"T1"},{"title":"T2"}]
    }
    mock_create.return_value = "PRJ-123"

    resp = client.post("/webhook/mattermost", data={
        "token": app.config["MATTERMOST_TOKEN"],
        "text": "start Demo WF"
    })
    assert resp.status_code == 200
    mock_create.assert_called_once_with("Demo WF", [{"title":"T1"},{"title":"T2"}])
    mock_send.assert_called_once()

def test_bad_token(client):
    resp = client.post("/webhook/mattermost", data={"token":"wrong"})
    assert resp.status_code == 403
