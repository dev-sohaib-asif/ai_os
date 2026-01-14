from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # OpenCode.Zen API
    opencode_zen_api_key: str
    opencode_zen_base_url: str = "https://api.opencode.zen/v1"
    opencode_zen_model: str = "bigpickle"
    
    # EMO Personality
    emo_name: str = "EMO"
    emo_personality: str = "cute_innocent"
    max_response_length: int = 200
    temperature: float = 0.8
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
