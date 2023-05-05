import os

import pytest
# we imported Starlette's TestClient, which uses the HTTPX library to make requests against the FastAPI app.
from starlette.testclient import TestClient
from app.config import get_settings, Settings
from app.main import create_application
from tortoise.contrib.fastapi import register_tortoise

def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    """To override the dependencies, we used the dependency_overrides attribute:
        dependency_overrides is a dict of key/value pairs where the key is the dependency name and the value is what we'd like to override it with
        key: get_settings
        value: get_settings_override """
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:
        # testing
        yield test_client



@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down