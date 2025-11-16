from app.config import settings
import math
import json
import os

# Cache for school data (loaded once at startup)
_SCHOOLS_CACHE = None


def load_schools_data():
    """
    Load Atlanta Public Schools data from JSON file
    Data is cached after first load for performance
    Source: Atlanta Public Schools directory + Open Data Portal
    """
    global _SCHOOLS_CACHE
    
    if _SCHOOLS_CACHE is None:
        # Get the path to the data file
        current_dir = os.path.dirname(__file__)
        data_path = os.path.join(current_dir, '../data/atlanta_schools.json')
        
        # Load the JSON file
        with open(data_path, 'r') as f:
            data = json.load(f)
            _SCHOOLS_CACHE = data['schools']
            print(f"✅ Loaded {len(_SCHOOLS_CACHE)} schools from atlanta_schools.json")
    
    return _SCHOOLS_CACHE


def calculate_school_impact(location, units):
    """
    Calculate school impact using Atlanta Public Schools data
    Data source: JSON file from Atlanta Public Schools directory (48 schools)
    """
    students = units * settings.STUDENTS_PER_UNIT
    
    # ✅ Load schools from JSON file (cached after first load)
    all_schools = load_schools_data()
    
    schools = []
    bottlenecks = []
    
    # Grade level distribution (industry standard)
    elementary_students = students * 0.4
    middle_students = students * 0.3
    high_students = students * 0.3
    
    for school_data in all_schools:
        # Calculate ACTUAL distance from clicked location
        distance = calculate_distance(
            location.lat, location.lng,
            school_data["lat"], school_data["lng"]
        )
        
        # Only include schools within 2.5 miles (realistic catchment area)
        if distance > 4000:  # 2.5 miles in meters
            continue
        
        # Determine which students go to this school based on grade level
        if school_data["grade_level"] == "elementary":
            new_students = elementary_students
        elif school_data["grade_level"] == "middle":
            new_students = middle_students
        else:  # high
            new_students = high_students
        
        # Calculate new enrollment and capacity percentage
        new_enrollment = school_data["enrollment"] + new_students
        capacity_pct = (new_enrollment / school_data["capacity"]) * 100
        
        school_info = {
            "name": school_data["name"],
            "distance": round(distance, 1),
            "grade_level": school_data["grade_level"],
            "enrollment": school_data["enrollment"],
            "capacity": school_data["capacity"],
            "capacity_pct": round(capacity_pct, 1)
        }
        schools.append(school_info)
        
        # Identify bottlenecks (schools over capacity)
        if capacity_pct > 100:
            severity = "HIGH" if capacity_pct > 120 else "MEDIUM"
            bottlenecks.append({
                "school": school_data["name"],
                "capacity_pct": round(capacity_pct, 1),
                "severity": severity,
                "message": f"{school_data['name']} will be at {capacity_pct:.0f}% capacity"
            })
    
    # Sort by distance (nearest first)
    schools.sort(key=lambda s: s["distance"])
    
    return {
        "students_generated": round(students, 1),
        "schools": schools,
        "bottlenecks": bottlenecks
    }


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns: Distance in meters
    """
    R = 6371000  # Earth radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c