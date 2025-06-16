from fastapi import FastAPI

@app.on_event("startup")
async def on_startup():
    print("🚀 Middleware is starting up...")

@app.on_event("shutdown")
async def on_shutdown():
 
    print("🛑 Middleware is shutting down...")


if __name__ == "__main__":
    import uvicorn
    # reload=True is only for development; disable in production
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )