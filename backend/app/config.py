from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "CityTrotter"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Keys - DEFAULT EMPTY (actual keys go in .env)
    GEMINI_API_KEY: str = ""
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # Analysis Parameters (Industry Standards)
    STUDENTS_PER_UNIT: float = 0.3
    WATER_DEMAND_GPD_PER_UNIT: float = 150
    TRIPS_PER_UNIT: float = 9.57
    AM_PEAK_RATIO: float = 0.11
    PM_PEAK_RATIO: float = 0.12
    PROPERTY_TAX_RATE: float = 0.011
    WALK_SPEED_MS: float = 1.4
    
    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()