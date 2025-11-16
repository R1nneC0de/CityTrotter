import math


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


def analyze_economic_impact(location, units, stories):
    """
    Calculate economic impact with location-based property values
    Property values vary by distance from downtown
    """
    # Downtown Atlanta (Five Points)
    downtown_lat, downtown_lng = 33.7590, -84.3880
    
    # Calculate distance from downtown
    distance_from_downtown = calculate_distance(
        location.lat, location.lng,
        downtown_lat, downtown_lng
    )
    
    # Property value decreases with distance from downtown
    # Downtown: $350k/unit, Suburbs: $200k/unit
    # Formula: Base $350k - $15k per km from downtown, min $180k
    distance_km = distance_from_downtown / 1000
    base_value_per_unit = max(180000, 350000 - (distance_km * 15000))
    
    total_property_value = units * base_value_per_unit
    
    # Atlanta millage rate: ~10.82 mills (1.082%)
    annual_tax_revenue = int(total_property_value * 0.01082)
    
    # Construction jobs: 1 job per 2 units for 18 months
    construction_jobs = int(units / 2)
    
    # Permanent jobs: Varies by location
    # Downtown = more retail/services = more jobs
    job_multiplier = 0.15 if distance_km < 2 else 0.10
    permanent_jobs = int(units * job_multiplier)
    
    # Infrastructure cost varies by location
    # Downtown = higher costs (dense, complex utilities)
    infrastructure_base_cost = 5000
    if distance_km < 2:
        infrastructure_cost_per_unit = infrastructure_base_cost + 2000  # Downtown premium
    elif distance_km < 5:
        infrastructure_cost_per_unit = infrastructure_base_cost + 1000  # Inner city
    else:
        infrastructure_cost_per_unit = infrastructure_base_cost  # Suburbs
    
    infrastructure_cost = units * infrastructure_cost_per_unit
    
    # Break-even calculation
    years_to_breakeven = round(infrastructure_cost / annual_tax_revenue, 1) if annual_tax_revenue > 0 else 99
    
    return {
        "total_property_value": int(total_property_value),
        "annual_tax_revenue": annual_tax_revenue,
        "infrastructure_cost": infrastructure_cost,
        "construction_jobs": construction_jobs,
        "permanent_jobs": permanent_jobs,
        "years_to_breakeven": years_to_breakeven
    }