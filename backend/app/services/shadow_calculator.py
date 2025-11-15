"""
Shadow analysis calculator service
"""

from app.models.analysis import Location, ShadowAnalysis
from typing import List
import math


def calculate_shadows(location: Location, footprint: List[List[float]], stories: int) -> ShadowAnalysis:
    """
    Calculate shadow impact at different times of day
    
    Args:
        location: Geographic location
        footprint: Building footprint polygon [[lng, lat], ...]
        stories: Number of stories
    
    Returns:
        ShadowAnalysis with shadow projections
    """
    
    building_height = stories * 12  # feet (12 ft per story)
    
    # Sun positions for Atlanta (33.7°N) on summer solstice (worst case)
    sun_positions = [
        {"time": "9:00 AM", "azimuth": 120, "altitude": 25},
        {"time": "12:00 PM", "azimuth": 180, "altitude": 55},
        {"time": "3:00 PM", "azimuth": 240, "altitude": 35},
        {"time": "5:00 PM", "azimuth": 270, "altitude": 15}
    ]
    
    shadows_by_time = []
    affected_parcels_set = set()
    
    for sun in sun_positions:
        # Calculate shadow length
        altitude_rad = math.radians(sun["altitude"])
        shadow_length = building_height / math.tan(altitude_rad)
        
        # Calculate shadow polygon (simplified - just extending footprint)
        # In production, would use proper 3D geometry projection
        shadow_area_sqft = calculate_footprint_area(footprint) * (1 + shadow_length / 100)
        
        # Mock affected parcels (would use PostGIS intersection query)
        affected_count = int(shadow_area_sqft / 5000)  # Rough estimate
        
        shadows_by_time.append({
            "time": sun["time"],
            "shadow_area_sqft": shadow_area_sqft,
            "affected_parcels": affected_count,
            "shadow_geometry": footprint  # Simplified - would be actual shadow polygon
        })
        
        affected_parcels_set.add(affected_count)
    
    return ShadowAnalysis(
        shadows_by_time=shadows_by_time,
        total_affected_parcels=sum(affected_parcels_set)
    )


def calculate_footprint_area(footprint: List[List[float]]) -> float:
    """
    Calculate area of polygon footprint using Shoelace formula
    
    Args:
        footprint: Polygon coordinates [[lng, lat], ...]
    
    Returns:
        Area in square feet (approximate)
    """
    if len(footprint) < 3:
        return 0
    
    # Shoelace formula
    area = 0
    for i in range(len(footprint)):
        j = (i + 1) % len(footprint)
        area += footprint[i][0] * footprint[j][1]
        area -= footprint[j][0] * footprint[i][1]
    
    area = abs(area) / 2.0
    
    # Convert from degrees to approximate square feet
    # (Very rough approximation - proper calculation would use projected coordinates)
    area_sqft = area * 10000000  # Rough conversion factor
    
    return area_sqft
