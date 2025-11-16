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
from app.services.heatmap_generator import generate_impact_heatmap

router = APIRouter()


@router.post("/analyze-building")
async def analyze_building(building: BuildingRequest):
    """Comprehensive building impact analysis"""
    try:
        building_id = str(uuid.uuid4())
        
        # Run all analyses
        zoning_result = zoning_checker.check_zoning(building.location, building.stories, building.units)
        school_impact = school_analyzer.calculate_school_impact(building.location, building.units)
        traffic_impact = traffic_calculator.calculate_traffic(building.location, building.units)
        transit_access = transit_analyzer.analyze_transit_access(building.location)
        infrastructure = infrastructure_analyzer.calculate_infrastructure_impact(building.location, building.units)
        shadow_analysis = shadow_calculator.calculate_shadows(building.location, building.footprint, building.stories)
        
        # ✅ FIXED: Call analyze_economic_impact with location parameter
        economic_impact = economic_analyzer.analyze_economic_impact(building.location, building.units, building.stories)
        
        # Aggregate results
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
        
        # Identify bottlenecks
        bottlenecks = identify_bottlenecks(all_results)
        
        # Generate AI report
        ai_report = await gemini_service.generate_planning_report(all_results)
        
        # Return complete analysis
        return {
            "building_id": building_id,
            "zoning": zoning_result,
            "school_impact": school_impact,
            "traffic_impact": traffic_impact,
            "transit_access": transit_access,
            "infrastructure": infrastructure,
            "shadow_analysis": shadow_analysis,
            "economic_impact": economic_impact,
            "bottlenecks": bottlenecks,
            "ai_report": ai_report
        }
        
    except Exception as e:
        print(f"ERROR in analyze_building: {str(e)}")  # Debug
        import traceback
        traceback.print_exc()  # Print full traceback
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def identify_bottlenecks(results: dict) -> list:
    """Identify critical bottlenecks from analysis results"""
    bottlenecks = []
    
    # Check zoning violations (now dict, not object)
    if not results["zoning"]["compliant"]:
        bottlenecks.append({
            "type": "ZONING",
            "severity": "HIGH",
            "message": f"Zoning violations: {', '.join(results['zoning']['violations'])}"
        })
    
    # Check school capacity (now dict)
    if results["school_impact"]["bottlenecks"]:
        for school in results["school_impact"]["bottlenecks"]:
            bottlenecks.append({
                "type": "SCHOOL_CAPACITY",
                "severity": school["severity"],
                "message": school["message"]
            })
    
    # Check traffic impact (now dict)
    if results["traffic_impact"]["los_impacts"]:
        bottlenecks.append({
            "type": "TRAFFIC",
            "severity": "HIGH",
            "message": f"{len(results['traffic_impact']['los_impacts'])} intersections degraded"
        })
    
    # Check infrastructure (now dict)
    if not results["infrastructure"]["infrastructure_adequate"]:
        bottlenecks.append({
            "type": "INFRASTRUCTURE",
            "severity": "MEDIUM",
            "message": f"Upgrades needed: {', '.join(results['infrastructure']['upgrades_needed'])}"
        })
    
    return bottlenecks

@router.get("/impact-heatmap")
async def get_impact_heatmap():
    """Get development impact heatmap data"""
    try:
        heatmap_data = generate_impact_heatmap()
        return heatmap_data
    except Exception as e:
        print(f"ERROR in heatmap generation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))