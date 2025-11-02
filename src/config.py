from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    model_name: str = "llama3.2"

    model_config = {"env_file": ".env"}


settings = Settings()
