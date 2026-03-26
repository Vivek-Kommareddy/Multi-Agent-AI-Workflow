from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mock_tools: bool = True
    mock_llm: bool = True
    ollama_base_url: str = "http://localhost:11434"
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        extra = "ignore"
