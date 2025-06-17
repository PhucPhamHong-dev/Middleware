import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Mattermost
    MATTERMOST_TOKEN      = os.getenv("MATTERMOST_TOKEN")
    MATTERMOST_WEBHOOK_URL= os.getenv("MATTERMOST_WEBHOOK_URL")

    # AI/NLP Engine
    AI_ENGINE_URL         = os.getenv("AI_ENGINE_URL")
    AI_ENGINE_KEY         = os.getenv("AI_ENGINE_KEY")

    # ERPNext
    ERPNEXT_URL           = os.getenv("ERPNEXT_URL")
    ERPNEXT_API_KEY       = os.getenv("ERPNEXT_API_KEY")
    ERPNEXT_API_SECRET    = os.getenv("ERPNEXT_API_SECRET")

    # App
    PORT                  = int(os.getenv("FLASK_PORT", 5000))
