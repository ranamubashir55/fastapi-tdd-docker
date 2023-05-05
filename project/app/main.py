from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise
from config import get_settings, Settings
import uvicorn, os

app = FastAPI()

# set up Tortoise-orm on startup and clean up on teardown:
register_tortoise(
    app,
    db_url=os.environ.get("DATABASE_URL"),
    modules={"models": ["models.tortoise"]},
    generate_schemas=False,  # if sets True then tables will create automatically if False then migration will happen using Aerich in db.py
    add_exception_handlers=True,
)


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
