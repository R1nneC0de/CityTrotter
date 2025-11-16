"""
Generate heatmap data for development impact visualization
"""

def generate_impact_heatmap():
    """
    Generate impact zones for Atlanta
    Simplified approach with pre-defined zones
    """
    
    features = []
    
    # Define impact zones manually (faster than grid calculation)
    zones = [
        # HIGH IMPACT ZONES (Red/Orange) - Dense urban areas
        {"center": [33.7590, -84.3880], "radius": 0.02, "score": 85, "name": "Downtown"},
        {"center": [33.7810, -84.3860], "radius": 0.015, "score": 80, "name": "Midtown"},
        {"center": [33.7650, -84.3480], "radius": 0.012, "score": 75, "name": "Virginia Highland"},
        {"center": [33.8470, -84.3650], "radius": 0.015, "score": 70, "name": "Buckhead"},
        
        # MEDIUM IMPACT ZONES (Yellow) - Developing areas
        {"center": [33.7480, -84.3350], "radius": 0.015, "score": 55, "name": "East Atlanta"},
        {"center": [33.7550, -84.4250], "radius": 0.015, "score": 50, "name": "West End"},
        {"center": [33.8180, -84.3620], "radius": 0.012, "score": 45, "name": "Brookhaven"},
        
        # LOW IMPACT ZONES (Green) - Suburban/less dense
        {"center": [33.8420, -84.3780], "radius": 0.015, "score": 30, "name": "North Buckhead"},
        {"center": [33.7280, -84.3680], "radius": 0.015, "score": 25, "name": "Grant Park"},
        {"center": [33.7150, -84.4500], "radius": 0.015, "score": 20, "name": "Southwest Atlanta"},
    ]
    
    for zone in zones:
        lat, lng = zone["center"]
        radius = zone["radius"]
        score = zone["score"]
        
        # Create circular zone (simplified as square for performance)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [lng - radius, lat - radius],
                    [lng + radius, lat - radius],
                    [lng + radius, lat + radius],
                    [lng - radius, lat + radius],
                    [lng - radius, lat - radius]
                ]]
            },
            "properties": {
                "impact_score": score,
                "zone_name": zone["name"]
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }