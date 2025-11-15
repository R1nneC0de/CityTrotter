"""
Building analysis API endpoints
"""

from fastapi import APIRouter, HTTPException
from app.models.analysis import BuildingRequest, BuildingAnalysisResponse
from app.services import (
    zoning_checker,
    school_analyzer,
    traffic_calculator,
    transit_analyzer,
    infrastructure_analyzer,
    shadow_calculator,
    economic_analyzer,
    gemini_service
)
import uuid
from datetime import datetime

router = APIRouter()


@router.post("/analyze-building", response_model=BuildingAnalysisResponse)
async def analyze_building(building: BuildingRequest):
    """
    Comprehensive building impact analysis
    
    Analyzes:
    - Zoning compliance
    - School capacity impact
    - Traffic generation
    - Transit access
    - Infrastructure capacity
    - Shadow impact
    - Economic impact
    - AI-generated summary
    """
    try:
        # Generate unique building ID
        building_id = str(uuid.uuid4())
        
        # Run all analyses (these will be implemented in services)
        # For now, returning mock data structure
        
        # 1. Zoning check
        zoning_result = zoning_checker.check_zoning(
            building.location,
            building.stories,
            building.units
        )
        
        # 2. School impact
        school_impact = school_analyzer.calculate_school_impact(
            building.location,
            building.units
        )
        
        # 3. Traffic impact
        traffic_impact = traffic_calculator.calculate_traffic(
            building.location,
            building.units
        )
        
        # 4. Transit access
        transit_access = transit_analyzer.analyze_transit_access(
            building.location
        )
        
        # 5. Infrastructure capacity
        infrastructure = infrastructure_analyzer.calculate_infrastructure_impact(
            building.location,
            building.units
        )
        
        # 6. Shadow analysis
        shadow_analysis = shadow_calculator.calculate_shadows(
            building.location,
            building.footprint,
            building.stories
        )
        
        # 7. Economic impact
        economic_impact = economic_analyzer.calculate_economic_impact(
            building.units,
            building.stories,
            infrastructure.estimated_cost
        )
        
        # Aggregate all results
        all_results = {
            "building_id": building_id,
            "building": building.dict(),
            "zoning": zoning_result,
            "school_impact": school_impact,
            "traffic_impact": traffic_impact,
            "transit_access": transit_access,
            "infrastructure": infrastructure,
            "shadow_analysis": shadow_analysis,
            "economic_impact": economic_impact
        }
        
        # 8. Identify bottlenecks
        bottlenecks = identify_bottlenecks(all_results)
        
        # 9. Generate AI report
        ai_report = await gemini_service.generate_planning_report(all_results)
        
        # Return complete analysis
        return BuildingAnalysisResponse(
            building_id=building_id,
            zoning=zoning_result,
            school_impact=school_impact,
            traffic_impact=traffic_impact,
            transit_access=transit_access,
            infrastructure=infrastructure,
            shadow_analysis=shadow_analysis,
            economic_impact=economic_impact,
            bottlenecks=bottlenecks,
            ai_report=ai_report
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def identify_bottlenecks(results: dict) -> list:
    """
    Identify critical bottlenecks from analysis results
    """
    bottlenecks = []
    
    # Check zoning violations
    if not results["zoning"].compliant:
        bottlenecks.append({
            "type": "ZONING",
            "severity": "HIGH",
            "message": f"Zoning violations: {', '.join(results['zoning'].violations)}"
        })
    
    # Check school capacity
    if results["school_impact"].bottlenecks:
        for school in results["school_impact"].bottlenecks:
            bottlenecks.append({
                "type": "SCHOOL_CAPACITY",
                "severity": school["severity"],
                "message": school["message"]
            })
    
    # Check traffic impact
    if results["traffic_impact"].los_impacts:
        bottlenecks.append({
            "type": "TRAFFIC",
            "severity": "HIGH",
            "message": f"{len(results['traffic_impact'].los_impacts)} intersections degraded"
        })
    
    # Check infrastructure
    if not results["infrastructure"].infrastructure_adequate:
        bottlenecks.append({
            "type": "INFRASTRUCTURE",
            "severity": "MEDIUM",
            "message": f"Upgrades needed: {', '.join(results['infrastructure'].upgrades_needed)}"
        })
    
    return bottlenecks


@router.get("/building/{building_id}")
async def get_building_analysis(building_id: str):
    """
    Retrieve previously stored building analysis
    TODO: Implement database retrieval
    """
    raise HTTPException(status_code=501, detail="Not yet implemented")
