from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODEL: str = "claude-haiku-5-5"
    MCP_URL: str = "http://localhost:8000/mcp"


settings = Settings()
