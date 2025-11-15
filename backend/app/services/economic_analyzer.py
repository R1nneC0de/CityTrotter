"""
Economic impact analyzer service
"""

from app.models.analysis import EconomicImpact
from app.config import settings


def calculate_economic_impact(units: int, stories: int, infrastructure_cost: float) -> EconomicImpact:
    """
    Calculate economic impact of development
    
    Analyzes:
    - Property tax revenue
    - Infrastructure costs
    - Job creation
    - Break-even timeline
    
    Args:
        units: Number of residential units
        stories: Number of stories
        infrastructure_cost: Cost of infrastructure upgrades
    
    Returns:
        EconomicImpact with analysis results
    """
    
    # Revenue calculation
    avg_monthly_rent = 2000  # Atlanta apartment average
    annual_rent_revenue = units * avg_monthly_rent * 12
    
    # Estimate property value (20x annual rent is common)
    estimated_property_value = annual_rent_revenue * 20
    
    # Calculate annual tax revenue (Atlanta rate: 1.1%)
    annual_tax_revenue = estimated_property_value * settings.PROPERTY_TAX_RATE
    
    # Job creation estimates
    # Construction: rough rule of thumb
    construction_jobs = int((units * stories) / 2)
    
    # Permanent jobs: property management, maintenance, retail
    permanent_jobs = max(int(units / 50), 1)  # 1 per 50 units minimum
    
    # Calculate break-even
    if annual_tax_revenue > 0:
        years_to_breakeven = infrastructure_cost / annual_tax_revenue
    else:
        years_to_breakeven = float('inf')
    
    # Net impact year 1 (revenue minus one-time costs)
    net_impact_year_1 = annual_tax_revenue - infrastructure_cost
    
    return EconomicImpact(
        annual_tax_revenue=annual_tax_revenue,
        infrastructure_cost=infrastructure_cost,
        net_impact_year_1=net_impact_year_1,
        years_to_breakeven=round(years_to_breakeven, 1),
        construction_jobs=construction_jobs,
        permanent_jobs=permanent_jobs
    )
