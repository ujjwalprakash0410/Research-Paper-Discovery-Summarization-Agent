from pydantic_settings import BaseSettings, SettingsConfigDict
"""
Centralized application configuration.

Loads settings from the .env file using Pydantic Settings.
"""

class Settings(BaseSettings):
    groq_api_key: str
    tavily_api_key: str

    langchain_api_key: str
    langchain_tracing_v2: bool = True
    langchain_project: str = "research-agent"

    llm_model: str = "llama-3.1-8b-instant"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 4

    max_search_results: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()