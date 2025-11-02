from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    model_name: str = "llama3.2"
    database_url: str = (
        "postgresql+asyncpg://llama_user:llama_pass@localhost:5432/llama_db"
    )

    model_config = {"env_file": ".env"}


settings = Settings()
