from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
    serper_api_key: str
    
    # App Config
    app_name: str = "Research & Blog Crew"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Limits
    max_concurrent_jobs: int = 5
    max_topic_length: int = 200
    rate_limit_per_user: int = 10  # per hour
    
    # Output
    output_dir: str = "output"
    log_dir: str = "logs"
    
    # Crew Settings
    crew_max_rpm: int = 30
    crew_memory: bool = True
    crew_cache: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()