from fastapi import FastAPI, Request
from nlp.nlp_handler import analyze_text
from erp.erp_handler import handle_intent

# Initialize the FastAPI application
app = FastAPI(
    title="Middleware API",
    description="Middleware between Mattermost, NLP Engine, and ERPNext",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.
    """
    print("🚀 Middleware is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler for application shutdown.
    """
    print("🛑 Middleware is shutting down...")

@app.post("/webhook/mattermost")
async def mattermost_webhook(request: Request):
    """
    Endpoint to handle incoming webhooks from Mattermost.
    """
    payload = await request.json()
    text = payload.get("text", "")
    nlp_result = analyze_text(text)
    erp_result = handle_intent(nlp_result)
    return {
        "nlp": nlp_result,
        "erp": erp_result
    }

@app.get("/")
async def root():
    """
    Root endpoint to verify that the application is running.
    """
    return {"message": "Middleware is running"}

if __name__ == "__main__":
    import uvicorn
    # Run the application using Uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
