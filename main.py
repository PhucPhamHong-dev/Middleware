import logging
import os
import sys
from fastapi import FastAPI
from handlers import mattermost_handler

# Set up logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "middleware.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(title="Middleware Integration")
app.include_router(mattermost_handler.router, prefix="/webhook")

@app.get("/")
async def root():
    return {"message": "Middleware is running..."}

@app.on_event("startup")
async def on_startup():
    logger.info("🚀 Middleware is starting...")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("🛑 Middleware is shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
