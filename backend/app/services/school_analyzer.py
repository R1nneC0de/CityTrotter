"""
School impact analysis service
"""

from app.models.analysis import Location, SchoolImpact, SchoolInfo
from app.config import settings
import math


def calculate_school_impact(location: Location, units: int) -> SchoolImpact:
    """
    Calculate impact on nearby schools
    
    Uses industry standard: 0.3 students per residential unit
    
    Args:
        location: Geographic location
        units: Number of residential units
    
    Returns:
        SchoolImpact with analysis results
    """
    
    # Calculate students generated (industry standard)
    students_generated = units * settings.STUDENTS_PER_UNIT
    
    # Grade level distribution (typical)
    elementary_students = students_generated * 0.4  # 40%
    middle_students = students_generated * 0.3      # 30%
    high_students = students_generated * 0.3        # 30%
    
    # TODO: Query PostGIS for schools within 1.5 mile radius
    # For MVP, using mock Atlanta schools data
    
    mock_schools = [
        {
            "name": "Grady High School",
            "lat": 33.7850,
            "lng": -84.3820,
            "grade_level": "high",
            "enrollment": 1800,
            "capacity": 1600
        },
        {
            "name": "Inman Middle School",
            "lat": 33.7740,
            "lng": -84.3530,
            "grade_level": "middle",
            "enrollment": 850,
            "capacity": 900
        },
        {
            "name": "Morningside Elementary",
            "lat": 33.7890,
            "lng": -84.3550,
            "grade_level": "elementary",
            "enrollment": 550,
            "capacity": 600
        }
    ]
    
    schools = []
    bottlenecks = []
    
    for school_data in mock_schools:
        # Calculate distance (simplified Haversine)
        distance = calculate_distance(
            location.lat, location.lng,
            school_data["lat"], school_data["lng"]
        )
        
        # Only include schools within 1.5 miles
        if distance > 2414:  # 1.5 miles in meters
            continue
        
        # Calculate new enrollment
        if school_data["grade_level"] == "elementary":
            new_students = elementary_students
        elif school_data["grade_level"] == "middle":
            new_students = middle_students
        else:  # high
            new_students = high_students
        
        new_enrollment = school_data["enrollment"] + new_students
        capacity_pct = (new_enrollment / school_data["capacity"]) * 100
        
        school_info = SchoolInfo(
            name=school_data["name"],
            distance=distance,
            grade_level=school_data["grade_level"],
            enrollment=school_data["enrollment"],
            capacity=school_data["capacity"],
            capacity_pct=capacity_pct
        )
        schools.append(school_info)
        
        # Identify bottlenecks (over 100% capacity)
        if capacity_pct > 100:
            severity = "HIGH" if capacity_pct > 120 else "MEDIUM"
            bottlenecks.append({
                "school": school_data["name"],
                "capacity_pct": capacity_pct,
                "severity": severity,
                "message": f"{school_data['name']} will be at {capacity_pct:.0f}% capacity"
            })
    
    return SchoolImpact(
        students_generated=students_generated,
        schools=schools,
        bottlenecks=bottlenecks
    )


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    
    Returns:
        Distance in meters
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
