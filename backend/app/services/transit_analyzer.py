"""
Transit access analyzer service
"""

from app.models.analysis import Location, TransitAccess, TransitStation
from app.config import settings
from app.services.school_analyzer import calculate_distance


def analyze_transit_access(location: Location) -> TransitAccess:
    """
    Analyze transit access to MARTA stations
    
    Args:
        location: Geographic location
    
    Returns:
        TransitAccess with analysis results
    """
    
    # TODO: Query PostGIS for MARTA stations
    # For MVP, using mock MARTA station data
    
    mock_stations = [
        {
            "name": "Arts Center",
            "line": "Red/Gold",
            "lat": 33.7890,
            "lng": -84.3870
        },
        {
            "name": "Midtown",
            "line": "Red/Gold",
            "lat": 33.7810,
            "lng": -84.3860
        },
        {
            "name": "North Avenue",
            "line": "Red/Gold",
            "lat": 33.7720,
            "lng": -84.3870
        }
    ]
    
    stations = []
    
    for station_data in mock_stations:
        distance = calculate_distance(
            location.lat, location.lng,
            station_data["lat"], station_data["lng"]
        )
        
        station = TransitStation(
            name=station_data["name"],
            line=station_data["line"],
            distance=distance
        )
        stations.append(station)
    
    # Sort by distance
    stations.sort(key=lambda s: s.distance)
    
    # Get nearest station
    nearest = stations[0]
    
    # Calculate walk time (1.4 m/s average walk speed)
    walk_time_minutes = (nearest.distance / settings.WALK_SPEED_MS) / 60
    
    # Score transit access
    if walk_time_minutes < 5:
        score = "EXCELLENT"
    elif walk_time_minutes < 10:
        score = "GOOD"
    elif walk_time_minutes < 15:
        score = "FAIR"
    else:
        score = "POOR"
    
    return TransitAccess(
        nearest_station=nearest,
        walk_time_minutes=round(walk_time_minutes, 1),
        transit_score=score,
        nearby_stations=stations[:3]  # Top 3 nearest
    )
