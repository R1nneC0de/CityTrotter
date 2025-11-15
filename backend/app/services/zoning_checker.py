def check_zoning(location, stories, units):
    """
    Check zoning compliance
    Returns dict (not Pydantic object)
    """
    zone_code = "MR-3"
    max_height = 150
    building_height = stories * 12
    
    violations = []
    if building_height > max_height:
        violations.append(f"Height {building_height}ft exceeds {max_height}ft")
    
    # Return dict (not object)
    return {
        "zone": zone_code,
        "compliant": len(violations) == 0,
        "violations": violations,
        "max_height": max_height,
        "max_far": 4.0
    }