from app.config import settings
from app.services.school_analyzer import calculate_distance

def calculate_traffic(location, units):
    daily_trips = int(units * settings.TRIPS_PER_UNIT)
    am_peak_trips = int(daily_trips * settings.AM_PEAK_RATIO)
    pm_peak_trips = int(daily_trips * settings.PM_PEAK_RATIO)
    
    # Mock intersections with coordinates
    mock_intersections = [
        {"name": "Peachtree & 10th", "lat": 33.7800, "lng": -84.3850, "current_volume": 1400, "current_los": "D"},
        {"name": "Juniper & 10th", "lat": 33.7790, "lng": -84.3820, "current_volume": 900, "current_los": "C"},
        {"name": "Piedmont & 10th", "lat": 33.7785, "lng": -84.3730, "current_volume": 1100, "current_los": "D"},
        {"name": "Peachtree & 14th", "lat": 33.7880, "lng": -84.3860, "current_volume": 1200, "current_los": "D"}
    ]
    
    los_impacts = []
    
    for intersection in mock_intersections:
        # Calculate distance from building
        distance = calculate_distance(
            location.lat, location.lng,
            intersection["lat"], intersection["lng"]
        )
        
        # Only affect intersections within 1 mile (1600m)
        if distance > 1600:
            continue
        
        # Impact decreases with distance (inverse square law)
        impact_factor = 1 / (1 + (distance / 400) ** 2)
        trips_to_intersection = pm_peak_trips * impact_factor
        
        new_volume = intersection["current_volume"] + trips_to_intersection
        projected_los = calculate_los(new_volume)
        
        if projected_los > intersection["current_los"]:
            los_impacts.append({
                "name": intersection["name"],
                "distance": round(distance, 1),
                "current_los": intersection["current_los"],
                "projected_los": projected_los,
                "severity": "HIGH" if projected_los == "F" else "MEDIUM"
            })
    
    return {
        "daily_trips": daily_trips,
        "peak_trips": {"am": am_peak_trips, "pm": pm_peak_trips},
        "los_impacts": los_impacts
    }


def calculate_los(volume):
    """Calculate Level of Service"""
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