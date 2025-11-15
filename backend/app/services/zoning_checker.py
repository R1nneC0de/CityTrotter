"""
Zoning compliance checker service
"""

from app.models.analysis import Location, ZoningResult
from app.config import settings


def check_zoning(location: Location, stories: int, units: int) -> ZoningResult:
    """
    Check zoning compliance for proposed building
    
    Args:
        location: Geographic location
        stories: Number of stories
        units: Number of units
    
    Returns:
        ZoningResult with compliance status
    """
    
    # TODO: Query PostGIS for actual zoning at location
    # For MVP, using mock data based on Atlanta zoning codes
    
    # Mock zoning rules (Atlanta examples)
    zoning_rules = {
        "R-4": {"max_height": 35, "max_units_per_acre": 8},
        "C-1": {"max_height": 50, "max_far": 2.0},
        "MR-3": {"max_height": 150, "max_far": 4.0},
        "MR-5": {"max_height": 250, "max_far": 8.0}
    }
    
    # For demo, assume MR-3 zoning in Midtown
    zone_code = "MR-3"
    rules = zoning_rules[zone_code]
    
    violations = []
    building_height = stories * 12  # 12 feet per story
    
    # Check height restriction
    if building_height > rules["max_height"]:
        violations.append(
            f"Height {building_height}ft exceeds maximum {rules['max_height']}ft"
        )
    
    # Check FAR if applicable (would need lot size)
    # For now, assume compliant
    
    return ZoningResult(
        zone=zone_code,
        compliant=len(violations) == 0,
        violations=violations,
        max_height=rules.get("max_height"),
        max_far=rules.get("max_far")
    )
