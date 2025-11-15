"""
Infrastructure capacity analyzer service
"""

from app.models.analysis import Location, InfrastructureImpact
from app.config import settings


def calculate_infrastructure_impact(location: Location, units: int) -> InfrastructureImpact:
    """
    Calculate infrastructure capacity impact
    
    Analyzes:
    - Water demand
    - Sewer capacity
    - Power demand
    
    Args:
        location: Geographic location
        units: Number of residential units
    
    Returns:
        InfrastructureImpact with analysis results
    """
    
    # Calculate demands (industry standards)
    water_demand = units * settings.WATER_DEMAND_GPD_PER_UNIT  # gallons per day
    sewer_demand = water_demand * 0.8  # 80% becomes wastewater
    power_demand = units * 2.5  # kW per unit (average)
    
    # TODO: Query infrastructure database for water mains, sewer lines, substations
    # For MVP, using simplified capacity check
    
    # Mock infrastructure capacity (would come from GIS data)
    water_main_capacity = 50000  # gpd
    sewer_line_capacity = 45000  # gpd
    substation_capacity = 1000   # kW
    
    upgrades_needed = []
    cost_estimate = 0
    
    # Check water capacity (70% threshold)
    if water_demand > (water_main_capacity * 0.7):
        upgrades_needed.append("Water main upgrade required")
        cost_estimate += 500000  # Typical water main upgrade cost
    
    # Check sewer capacity
    if sewer_demand > (sewer_line_capacity * 0.7):
        upgrades_needed.append("Sewer line expansion needed")
        cost_estimate += 750000  # Typical sewer upgrade cost
    
    # Check power capacity
    if power_demand > (substation_capacity * 0.8):
        upgrades_needed.append("Electrical service upgrade required")
        cost_estimate += 300000  # Substation/transformer upgrade
    
    return InfrastructureImpact(
        water_demand=water_demand,
        sewer_demand=sewer_demand,
        power_demand=power_demand,
        upgrades_needed=upgrades_needed,
        estimated_cost=cost_estimate,
        infrastructure_adequate=len(upgrades_needed) == 0
    )
