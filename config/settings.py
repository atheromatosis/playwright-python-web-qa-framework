from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8000"
    HEADLESS: bool = True
    SLOW_MO: int = 0
    TIMEOUT: int = 10000  # ms

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()



# trigger linguist

"""Runtime configuration module."""

"""Runtime configuration module."""
