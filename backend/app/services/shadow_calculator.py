import math


def calculate_shadows(location, footprint, stories):
    """
    Calculate shadow impact
    Returns dict (not Pydantic object)
    """
    building_height = stories * 12
    
    sun_positions = [
        {"time": "9:00 AM", "azimuth": 120, "altitude": 25},
        {"time": "12:00 PM", "azimuth": 180, "altitude": 55},
        {"time": "3:00 PM", "azimuth": 240, "altitude": 35},
        {"time": "5:00 PM", "azimuth": 270, "altitude": 15}
    ]
    
    shadows_by_time = []
    affected_parcels_set = set()
    
    for sun in sun_positions:
        altitude_rad = math.radians(sun["altitude"])
        shadow_length = building_height / math.tan(altitude_rad)
        shadow_area_sqft = calculate_footprint_area(footprint) * (1 + shadow_length / 100)
        affected_count = int(shadow_area_sqft / 5000)
        
        shadows_by_time.append({
            "time": sun["time"],
            "shadow_area_sqft": shadow_area_sqft,
            "affected_parcels": affected_count,
            "shadow_geometry": footprint
        })
        
        affected_parcels_set.add(affected_count)
    
    # Return dict (not object)
    return {
        "shadows_by_time": shadows_by_time,
        "total_affected_parcels": sum(affected_parcels_set)
    }


def calculate_footprint_area(footprint):
    """Calculate area using Shoelace formula"""
    if len(footprint) < 3:
        return 0
    
    area = 0
    for i in range(len(footprint)):
        j = (i + 1) % len(footprint)
        area += footprint[i][0] * footprint[j][1]
        area -= footprint[j][0] * footprint[i][1]
    
    area = abs(area) / 2.0
    area_sqft = area * 10000000
    
    return area_sqft