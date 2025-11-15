from app.config import settings
import math


def calculate_school_impact(location, units):
    """Calculate school impact with dynamic distance calculations"""
    students = units * settings.STUDENTS_PER_UNIT
    
    all_schools = [
        {"name": "Grady High School", "lat": 33.7850, "lng": -84.3820, "grade_level": "high", "enrollment": 1800, "capacity": 1600},
        {"name": "Inman Middle School", "lat": 33.7740, "lng": -84.3530, "grade_level": "middle", "enrollment": 850, "capacity": 900},
        {"name": "Morningside Elementary", "lat": 33.7890, "lng": -84.3550, "grade_level": "elementary", "enrollment": 550, "capacity": 600},
        {"name": "Midtown High School", "lat": 33.7820, "lng": -84.3850, "grade_level": "high", "enrollment": 1500, "capacity": 1400},
        {"name": "Hope-Hill Elementary", "lat": 33.7650, "lng": -84.3720, "grade_level": "elementary", "enrollment": 480, "capacity": 500},
    ]
    
    schools = []
    bottlenecks = []
    
    elementary_students = students * 0.4
    middle_students = students * 0.3
    high_students = students * 0.3
    
    for school_data in all_schools:
        distance = calculate_distance(
            location.lat, location.lng,
            school_data["lat"], school_data["lng"]
        )
        
        if distance > 4000:
            continue
        
        if school_data["grade_level"] == "elementary":
            new_students = elementary_students
        elif school_data["grade_level"] == "middle":
            new_students = middle_students
        else:
            new_students = high_students
        
        new_enrollment = school_data["enrollment"] + new_students
        capacity_pct = (new_enrollment / school_data["capacity"]) * 100
        
        schools.append({
            "name": school_data["name"],
            "distance": distance,
            "grade_level": school_data["grade_level"],
            "enrollment": school_data["enrollment"],
            "capacity": school_data["capacity"],
            "capacity_pct": capacity_pct
        })
        
        if capacity_pct > 100:
            severity = "HIGH" if capacity_pct > 120 else "MEDIUM"
            bottlenecks.append({
                "school": school_data["name"],
                "capacity_pct": capacity_pct,
                "severity": severity,
                "message": f"{school_data['name']} will be at {capacity_pct:.0f}% capacity"
            })
    
    schools.sort(key=lambda s: s["distance"])
    
    return {
        "students_generated": students,
        "schools": schools,
        "bottlenecks": bottlenecks
    }


def calculate_distance(lat1, lng1, lat2, lng2):
    """Haversine distance calculation"""
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c