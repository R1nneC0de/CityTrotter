def analyze_transit_access(location):
    """Analyze MARTA transit access"""
    from app.services.school_analyzer import calculate_distance
    
    all_stations = [
        {"name": "Arts Center", "line": "Red/Gold", "lat": 33.7890, "lng": -84.3870},
        {"name": "Midtown", "line": "Red/Gold", "lat": 33.7810, "lng": -84.3860},
        {"name": "North Avenue", "line": "Red/Gold", "lat": 33.7720, "lng": -84.3870},
        {"name": "Civic Center", "line": "Red/Gold", "lat": 33.7660, "lng": -84.3870},
        {"name": "Peachtree Center", "line": "Red/Gold", "lat": 33.7590, "lng": -84.3880},
        {"name": "Five Points", "line": "All Lines", "lat": 33.7540, "lng": -84.3920},
        {"name": "Lindbergh Center", "line": "Red/Gold", "lat": 33.8230, "lng": -84.3690},
    ]
    
    stations = []
    for station_data in all_stations:
        distance = calculate_distance(
            location.lat, location.lng,
            station_data["lat"], station_data["lng"]
        )
        
        stations.append({
            "name": station_data["name"],
            "line": station_data["line"],
            "distance": distance
        })
    
    stations.sort(key=lambda s: s["distance"])
    nearest = stations[0]
    walk_time = (nearest["distance"] / 1.4) / 60
    
    if walk_time < 5:
        score = "EXCELLENT"
    elif walk_time < 10:
        score = "GOOD"
    elif walk_time < 15:
        score = "FAIR"
    else:
        score = "POOR"
    
    return {
        "nearest_station": nearest,
        "walk_time_minutes": round(walk_time, 1),
        "transit_score": score,
        "nearby_stations": stations[:3]
    }