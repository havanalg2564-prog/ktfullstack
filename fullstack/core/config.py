from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Для локальной разработки используем синхронный драйвер psycopg2
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/notes_db"
    SECRET_KEY: str = "your-super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()