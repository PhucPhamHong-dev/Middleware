
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
class MattermostPayload(BaseModel):
    token: str
    team_id: str
    channel_id: str
    user_name: str
    text: str
    command: str
def analyze_text(text: str) -> str:
    intent = "mock_intent"
    entities = ["entity1", "entity2"]
    return f"Intent: {intent}; Entities: {entities}; Original: {text}"
@app.post("/mattermost/webhook")
async def handle_mattermost(payload: MattermostPayload):
    if payload.token != "12345":
        raise HTTPException(status_code=403, detail="Invalid token")
    
   
    raw_text = payload.text.strip()

    
    analysis_result = analyze_text(raw_text)
    response_body = {
        "response_type": "in_channel",
        "text": analysis_result
    }
    return JSONResponse(content=response_body)
