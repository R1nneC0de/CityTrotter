"""
Data endpoints for serving geospatial data layers
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()


@router.get("/data/schools")
async def get_schools() -> Dict[str, Any]:
    """
    Get all Atlanta schools for map layer
    Returns GeoJSON FeatureCollection
    """
    # TODO: Query from database
    # For now, return empty GeoJSON
    return {
        "type": "FeatureCollection",
        "features": []
    }


@router.get("/data/zoning")
async def get_zoning() -> Dict[str, Any]:
    """
    Get Atlanta zoning boundaries for map layer
    Returns GeoJSON FeatureCollection
    """
    # TODO: Query from database
    return {
        "type": "FeatureCollection",
        "features": []
    }


@router.get("/data/marta-stations")
async def get_marta_stations() -> Dict[str, Any]:
    """
    Get MARTA station locations for map layer
    Returns GeoJSON FeatureCollection
    """
    # TODO: Query from database
    return {
        "type": "FeatureCollection",
        "features": []
    }


@router.get("/data/summary")
async def get_data_summary():
    """
    Get summary of available data layers
    """
    return {
        "schools": {
            "count": 0,
            "last_updated": None
        },
        "zoning": {
            "count": 0,
            "last_updated": None
        },
        "marta_stations": {
            "count": 0,
            "last_updated": None
        }
    }
