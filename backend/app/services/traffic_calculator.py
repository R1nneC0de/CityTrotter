from app.config import settings
from app.services.school_analyzer import calculate_distance

def calculate_traffic(location, units):
    """
    Calculate traffic impact using distance-based distribution
    Intersections across different Atlanta neighborhoods
    """
    daily_trips = int(units * settings.TRIPS_PER_UNIT)
    am_peak_trips = int(daily_trips * settings.AM_PEAK_RATIO)
    pm_peak_trips = int(daily_trips * settings.PM_PEAK_RATIO)
    
    # Real Atlanta intersections across different neighborhoods
    mock_intersections = [
        # MIDTOWN/DOWNTOWN
        {"name": "Peachtree & 10th", "lat": 33.7800, "lng": -84.3850, "current_volume": 1400, "current_los": "D"},
        {"name": "Juniper & 10th", "lat": 33.7790, "lng": -84.3820, "current_volume": 900, "current_los": "C"},
        {"name": "Piedmont & 10th", "lat": 33.7785, "lng": -84.3730, "current_volume": 1100, "current_los": "D"},
        {"name": "Peachtree & 14th", "lat": 33.7880, "lng": -84.3860, "current_volume": 1200, "current_los": "D"},
        {"name": "Spring & 5th", "lat": 33.7650, "lng": -84.3880, "current_volume": 1300, "current_los": "D"},
        
        # BUCKHEAD
        {"name": "Peachtree & Lenox", "lat": 33.8470, "lng": -84.3650, "current_volume": 1500, "current_los": "E"},
        {"name": "Roswell & Piedmont", "lat": 33.8420, "lng": -84.3710, "current_volume": 1200, "current_los": "D"},
        {"name": "Peachtree & Pharr", "lat": 33.8350, "lng": -84.3680, "current_volume": 1100, "current_los": "D"},
        
        # EAST ATLANTA
        {"name": "Moreland & Memorial", "lat": 33.7350, "lng": -84.3480, "current_volume": 1000, "current_los": "C"},
        {"name": "Boulevard & North", "lat": 33.7720, "lng": -84.3650, "current_volume": 900, "current_los": "C"},
        {"name": "DeKalb & Candler", "lat": 33.7520, "lng": -84.3380, "current_volume": 800, "current_los": "B"},
        
        # WEST ATLANTA
        {"name": "MLK & Northside", "lat": 33.7550, "lng": -84.4250, "current_volume": 1100, "current_los": "D"},
        {"name": "Simpson & Joseph Lowery", "lat": 33.7580, "lng": -84.4350, "current_volume": 950, "current_los": "C"},
        
        # SOUTH ATLANTA
        {"name": "Metropolitan & Pryor", "lat": 33.7150, "lng": -84.4050, "current_volume": 1000, "current_los": "C"},
        {"name": "University & McDaniel", "lat": 33.7250, "lng": -84.4150, "current_volume": 900, "current_los": "C"},
    ]
    
    los_impacts = []
    
    for intersection in mock_intersections:
        # Calculate distance from building
        distance = calculate_distance(
            location.lat, location.lng,
            intersection["lat"], intersection["lng"]
        )
        
        # Only affect intersections within 1.5 miles (2400m)
        if distance > 2400:
            continue
        
        # Impact decreases with distance (inverse square law)
        # Closer intersections get more traffic
        impact_factor = 1 / (1 + (distance / 400) ** 2)
        trips_to_intersection = pm_peak_trips * impact_factor
        
        new_volume = intersection["current_volume"] + trips_to_intersection
        projected_los = calculate_los(new_volume)
        
        # Only report if LOS degrades
        if projected_los > intersection["current_los"]:
            los_impacts.append({
                "name": intersection["name"],
                "distance": round(distance, 1),
                "current_los": intersection["current_los"],
                "projected_los": projected_los,
                "severity": "HIGH" if projected_los == "F" else "MEDIUM"
            })
    
    # Sort by severity (HIGH first) then distance (nearest first)
    los_impacts.sort(key=lambda x: (0 if x["severity"] == "HIGH" else 1, x["distance"]))
    
    return {
        "daily_trips": daily_trips,
        "peak_trips": {"am": am_peak_trips, "pm": pm_peak_trips},
        "los_impacts": los_impacts
    }


def calculate_los(volume):
    """
    Calculate Level of Service based on vehicle volume
    Industry standard: HCM (Highway Capacity Manual) metrics
    """
    if volume < 600:
        return "A"  # Free flow
    elif volume < 900:
        return "B"  # Reasonably free flow
    elif volume < 1200:
        return "C"  # Stable flow
    elif volume < 1400:
        return "D"  # Approaching unstable
    elif volume < 1600:
        return "E"  # Unstable flow
    else:
        return "F"  # Forced/breakdown flow