import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async  # new
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")

# Tortoise supports database migrations via Aerich
TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    # set up Tortoise-orm on startup and clean up on teardown:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,  # if sets True then tables will create automatically if False then migration will happen using Aerich in db.py
        add_exception_handlers=True,
    )


# generate_schema calls Tortoise.init to set up Tortoise and then generates the schema.
# to generate the schemas by calling below func run the below command in terminal
# docker-compose exec web python app/db.py
async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
