from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env into os.environ so that os.getenv() calls in tools see the same values
# as the pydantic Settings object. This is a no-op if the file doesn't exist.
_env_file = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_file, override=False)


class Settings(BaseSettings):
    mock_tools: bool = True
    mock_llm: bool = True
    ollama_base_url: str = "http://localhost:11434"
    redis_url: str = "redis://localhost:6379/0"
    tavily_api_key: str = ""
    serpapi_api_key: str = ""

    class Config:
        env_file = str(_env_file)
        extra = "ignore"
