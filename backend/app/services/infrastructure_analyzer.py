from app.config import settings


def calculate_infrastructure_impact(location, units):
    """
    Calculate infrastructure capacity impact
    Returns dict (not Pydantic object)
    """
    # Calculate demands (industry standards)
    water_demand = units * settings.WATER_DEMAND_GPD_PER_UNIT
    sewer_demand = water_demand * 0.8
    power_demand = units * 2.5
    
    # Mock infrastructure capacity
    water_main_capacity = 50000
    sewer_line_capacity = 45000
    substation_capacity = 1000
    
    upgrades_needed = []
    cost_estimate = 0
    
    # Check capacity (70% threshold)
    if water_demand > (water_main_capacity * 0.7):
        upgrades_needed.append("Water main upgrade required")
        cost_estimate += 500000
    
    if sewer_demand > (sewer_line_capacity * 0.7):
        upgrades_needed.append("Sewer line expansion needed")
        cost_estimate += 750000
    
    if power_demand > (substation_capacity * 0.8):
        upgrades_needed.append("Electrical service upgrade required")
        cost_estimate += 300000
    
    # Return dict (not object)
    return {
        "water_demand": water_demand,
        "sewer_demand": sewer_demand,
        "power_demand": power_demand,
        "upgrades_needed": upgrades_needed,
        "estimated_cost": cost_estimate,
        "infrastructure_adequate": len(upgrades_needed) == 0
    }