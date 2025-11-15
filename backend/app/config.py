"""
Configuration settings for CityTrotter backend
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "CityTrotter"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/citytrotter"
    
    # API Keys
    GEMINI_API_KEY: str = ""
    MAPBOX_TOKEN: str = ""
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Analysis Parameters
    STUDENTS_PER_UNIT: float = 0.3  # National average
    WATER_DEMAND_GPD_PER_UNIT: float = 150  # Gallons per day
    TRIPS_PER_UNIT: float = 9.57  # ITE Trip Generation Manual
    AM_PEAK_RATIO: float = 0.11  # 11% of daily trips
    PM_PEAK_RATIO: float = 0.12  # 12% of daily trips
    PROPERTY_TAX_RATE: float = 0.011  # Atlanta 1.1%
    WALK_SPEED_MS: float = 1.4  # meters per second
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create global settings instance
settings = get_settings()
