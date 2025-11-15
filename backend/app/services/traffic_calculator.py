"""
Traffic impact calculator service
Based on ITE Trip Generation Manual standards
"""

from app.models.analysis import Location, TrafficImpact, IntersectionImpact
from app.config import settings


def calculate_traffic(location: Location, units: int) -> TrafficImpact:
    """
    Calculate traffic impact using ITE Trip Generation Manual
    
    ITE Code 220 (Apartments): 9.57 trips per unit per day
    
    Args:
        location: Geographic location
        units: Number of residential units
    
    Returns:
        TrafficImpact with analysis results
    """
    
    # ITE Trip Generation Manual - Code 220 (Apartments)
    daily_trips = int(units * settings.TRIPS_PER_UNIT)
    
    # Peak hour calculations (ITE standards)
    am_peak_trips = int(daily_trips * settings.AM_PEAK_RATIO)  # 11% AM
    pm_peak_trips = int(daily_trips * settings.PM_PEAK_RATIO)  # 12% PM
    
    # TODO: Query OSM for nearby intersections
    # For MVP, using mock intersection data
    
    mock_intersections = [
        {
            "name": "Peachtree St & 10th St",
            "lat": 33.7800,
            "lng": -84.3850,
            "current_volume": 1400,  # vehicles per hour
            "current_los": "D"
        },
        {
            "name": "Juniper St & 10th St",
            "lat": 33.7795,
            "lng": -84.3820,
            "current_volume": 900,
            "current_los": "C"
        },
        {
            "name": "Piedmont Ave & 10th St",
            "lat": 33.7790,
            "lng": -84.3730,
            "current_volume": 1100,
            "current_los": "D"
        }
    ]
    
    # Distribute trips across intersections (simplified)
    trips_per_intersection = pm_peak_trips / len(mock_intersections)
    
    los_impacts = []
    
    for intersection in mock_intersections:
        new_volume = intersection["current_volume"] + trips_per_intersection
        projected_los = calculate_los(new_volume)
        
        # Check if LOS degrades
        if projected_los > intersection["current_los"]:
            los_impacts.append(IntersectionImpact(
                name=intersection["name"],
                current_los=intersection["current_los"],
                projected_los=projected_los,
                severity="HIGH" if projected_los == "F" else "MEDIUM"
            ))
    
    return TrafficImpact(
        daily_trips=daily_trips,
        peak_trips={"am": am_peak_trips, "pm": pm_peak_trips},
        los_impacts=los_impacts
    )


def calculate_los(volume: float) -> str:
    """
    Calculate Level of Service based on volume
    
    Based on Highway Capacity Manual thresholds
    
    Args:
        volume: Vehicles per hour
    
    Returns:
        LOS rating (A-F)
    """
    if volume < 600:
        return "A"
    elif volume < 900:
        return "B"
    elif volume < 1200:
        return "C"
    elif volume < 1400:
        return "D"
    elif volume < 1600:
        return "E"
    else:
        return "F"
