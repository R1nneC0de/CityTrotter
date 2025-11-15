from app.config import settings


def calculate_economic_impact(units, stories, infrastructure_cost):
    """
    Calculate economic impact
    Returns dict (not Pydantic object)
    """
    # Revenue calculation
    avg_monthly_rent = 2000
    annual_rent_revenue = units * avg_monthly_rent * 12
    estimated_property_value = annual_rent_revenue * 20
    annual_tax_revenue = estimated_property_value * settings.PROPERTY_TAX_RATE
    
    # Job creation
    construction_jobs = int((units * stories) / 2)
    permanent_jobs = max(int(units / 50), 1)
    
    # Break-even
    if annual_tax_revenue > 0:
        years_to_breakeven = infrastructure_cost / annual_tax_revenue
    else:
        years_to_breakeven = float('inf')
    
    net_impact_year_1 = annual_tax_revenue - infrastructure_cost
    
    # Return dict (not object)
    return {
        "annual_tax_revenue": annual_tax_revenue,
        "infrastructure_cost": infrastructure_cost,
        "net_impact_year_1": net_impact_year_1,
        "years_to_breakeven": round(years_to_breakeven, 1),
        "construction_jobs": construction_jobs,
        "permanent_jobs": permanent_jobs
    }