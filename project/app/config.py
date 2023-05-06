import logging
from functools import lru_cache

from pydantic import (  # BaseSettings automatically reads from environment variables for config settings
    AnyUrl, BaseSettings)

log = logging.getLogger("uvicorn")


# environment-specific configuration variables
class Settings(
    BaseSettings
):  # environment: str = "dev" is equivalent to environment: str = os.getenv("ENVIRONMENT", "dev")
    environment: str = "dev"  # e.g. dev, stage, prod
    testing: bool = bool(0)  # whether or not we're in test mode
    database_url: AnyUrl = None


@lru_cache()  # use lru_cache to cache the settings so get_settings is only called once
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
