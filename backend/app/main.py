"""
CityTrotter - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import building_analysis, data
import os

app = FastAPI(
    title="CityTrotter API",
    description="City Development Impact Analyzer",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(building_analysis.router, prefix="/api/v1", tags=["Building Analysis"])
app.include_router(data.router, prefix="/api/v1", tags=["Data"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "CityTrotter API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB check
        "services": "operational"
    }
