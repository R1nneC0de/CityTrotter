def analyze_transit_access(location):
    """
    Analyze MARTA transit access using REAL station locations
    Data source: Official MARTA rail station coordinates
    """
    from app.services.school_analyzer import calculate_distance
    
    # ✅ REAL MARTA STATIONS - All 38 rail stations
    all_stations = [
        # RED LINE (North-South)
        {"name": "North Springs", "line": "Red", "lat": 33.9929, "lng": -84.3576},
        {"name": "Sandy Springs", "line": "Red", "lat": 33.9316, "lng": -84.3513},
        {"name": "Dunwoody", "line": "Red", "lat": 33.9486, "lng": -84.3455},
        {"name": "Medical Center", "line": "Red", "lat": 33.9106, "lng": -84.3513},
        {"name": "Buckhead", "line": "Red", "lat": 33.8476, "lng": -84.3671},
        {"name": "Lindbergh Center", "line": "Red/Gold", "lat": 33.8230, "lng": -84.3690},
        {"name": "Arts Center", "line": "Red/Gold", "lat": 33.7890, "lng": -84.3870},
        {"name": "Midtown", "line": "Red/Gold", "lat": 33.7810, "lng": -84.3860},
        {"name": "North Avenue", "line": "Red/Gold", "lat": 33.7720, "lng": -84.3870},
        {"name": "Civic Center", "line": "Red/Gold", "lat": 33.7660, "lng": -84.3870},
        {"name": "Peachtree Center", "line": "Red/Gold", "lat": 33.7590, "lng": -84.3880},
        {"name": "Five Points", "line": "All Lines", "lat": 33.7540, "lng": -84.3920},
        {"name": "Garnett", "line": "Red/Gold", "lat": 33.7480, "lng": -84.3960},
        {"name": "West End", "line": "Red/Gold", "lat": 33.7358, "lng": -84.4129},
        {"name": "Oakland City", "line": "Red/Gold", "lat": 33.7171, "lng": -84.4260},
        {"name": "Lakewood/Fort McPherson", "line": "Red/Gold", "lat": 33.7002, "lng": -84.4260},
        {"name": "East Point", "line": "Red/Gold", "lat": 33.6768, "lng": -84.4397},
        {"name": "College Park", "line": "Red/Gold", "lat": 33.6513, "lng": -84.4493},
        {"name": "Airport", "line": "Red/Gold", "lat": 33.6397, "lng": -84.4443},
        
        # GOLD LINE (Northeast)
        {"name": "Doraville", "line": "Gold", "lat": 33.9026, "lng": -84.2797},
        {"name": "Chamblee", "line": "Gold", "lat": 33.8879, "lng": -84.3046},
        {"name": "Brookhaven", "line": "Gold", "lat": 33.8590, "lng": -84.3390},
        {"name": "Lenox", "line": "Gold", "lat": 33.8450, "lng": -84.3570},
        
        # GREEN LINE (East-West)
        {"name": "Bankhead", "line": "Green", "lat": 33.7723, "lng": -84.4285},
        {"name": "Ashby", "line": "Green", "lat": 33.7565, "lng": -84.4177},
        {"name": "Vine City", "line": "Green", "lat": 33.7563, "lng": -84.4040},
        {"name": "Dome/GWCC", "line": "Green/Blue", "lat": 33.7598, "lng": -84.3964},
        {"name": "Georgia State", "line": "Green/Blue", "lat": 33.7489, "lng": -84.3851},
        {"name": "King Memorial", "line": "Green/Blue", "lat": 33.7490, "lng": -84.3727},
        {"name": "Inman Park", "line": "Green/Blue", "lat": 33.7578, "lng": -84.3528},
        {"name": "Edgewood", "line": "Green/Blue", "lat": 33.7613, "lng": -84.3403},
        {"name": "East Lake", "line": "Green/Blue", "lat": 33.7650, "lng": -84.3140},
        {"name": "Decatur", "line": "Green/Blue", "lat": 33.7748, "lng": -84.2968},
        {"name": "Avondale", "line": "Green", "lat": 33.7715, "lng": -84.2806},
        {"name": "Kensington", "line": "Green", "lat": 33.7726, "lng": -84.2520},
        {"name": "Indian Creek", "line": "Green", "lat": 33.7693, "lng": -84.2291},
        
        # BLUE LINE (West)
        {"name": "Hamilton E. Holmes", "line": "Blue", "lat": 33.7548, "lng": -84.4699},
        {"name": "West Lake", "line": "Blue", "lat": 33.7530, "lng": -84.4461},
    ]
    
    stations = []
    for station_data in all_stations:
        # Calculate ACTUAL distance from clicked location
        distance = calculate_distance(
            location.lat, location.lng,
            station_data["lat"], station_data["lng"]
        )
        
        stations.append({
            "name": station_data["name"],
            "line": station_data["line"],
            "distance": round(distance, 1)
        })
    
    # Sort by distance (nearest first)
    stations.sort(key=lambda s: s["distance"])
    
    nearest = stations[0]
    
    # Calculate walk time (1.4 m/s = average walking speed)
    walk_time = (nearest["distance"] / 1.4) / 60  # Convert to minutes
    
    # Score based on walk time (industry standard)
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
        "nearby_stations": stations[:3]  # Top 3 nearest
    }