from app.config import settings


def calculate_traffic(location, units):
    """
    Calculate traffic impact using ITE standards
    Returns dict (not Pydantic object)
    """
    daily_trips = int(units * settings.TRIPS_PER_UNIT)
    am_peak_trips = int(daily_trips * settings.AM_PEAK_RATIO)
    pm_peak_trips = int(daily_trips * settings.PM_PEAK_RATIO)
    
    # Mock intersection data
    mock_intersections = [
        {"name": "Peachtree St & 10th St", "current_volume": 1400, "current_los": "D"},
        {"name": "Juniper St & 10th St", "current_volume": 900, "current_los": "C"},
        {"name": "Piedmont Ave & 10th St", "current_volume": 1100, "current_los": "D"}
    ]
    
    trips_per_intersection = pm_peak_trips / len(mock_intersections)
    los_impacts = []
    
    for intersection in mock_intersections:
        new_volume = intersection["current_volume"] + trips_per_intersection
        projected_los = calculate_los(new_volume)
        
        if projected_los > intersection["current_los"]:
            los_impacts.append({
                "name": intersection["name"],
                "current_los": intersection["current_los"],
                "projected_los": projected_los,
                "severity": "HIGH" if projected_los == "F" else "MEDIUM"
            })
    
    # Return dict (not object)
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