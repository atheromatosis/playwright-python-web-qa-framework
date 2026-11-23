from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8000"
    HEADLESS: bool = True
    SLOW_MO: int = 0
    TIMEOUT: int = 10000  # ms

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
