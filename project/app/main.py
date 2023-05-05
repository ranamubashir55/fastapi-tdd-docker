from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise
import sys, logging
sys.path.append("./")
from app.config import get_settings, Settings
import uvicorn, os
from app.api import ping, summaries
from app.db import init_db

log = logging.getLogger("uvicorn")

def create_application() -> FastAPI:
    application = FastAPI()

    application.include_router(ping.router)
    application.include_router(summaries.router, prefix="/summaries", tags=["summaries"])

    return application

app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
