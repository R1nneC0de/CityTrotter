"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Location(BaseModel):
    """Geographic location"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")


class BuildingRequest(BaseModel):
    """Request model for building analysis"""
    location: Location
    footprint: List[List[float]] = Field(..., description="Polygon coordinates [[lng, lat], ...]")
    type: str = Field(..., description="Building type: residential, commercial, mixed-use")
    units: int = Field(..., gt=0, description="Number of units")
    stories: int = Field(..., gt=0, le=100, description="Number of stories")
    parking_spaces: int = Field(..., ge=0, description="Number of parking spaces")


class ZoningResult(BaseModel):
    """Zoning compliance check result"""
    zone: str
    compliant: bool
    violations: List[str]
    max_height: Optional[int]
    max_far: Optional[float]


class SchoolInfo(BaseModel):
    """School information"""
    name: str
    distance: float
    grade_level: str
    enrollment: int
    capacity: int
    capacity_pct: float


class SchoolImpact(BaseModel):
    """School impact analysis result"""
    students_generated: float
    schools: List[SchoolInfo]
    bottlenecks: List[Dict[str, Any]]


class IntersectionImpact(BaseModel):
    """Traffic intersection impact"""
    name: str
    current_los: str
    projected_los: str
    severity: str


class TrafficImpact(BaseModel):
    """Traffic impact analysis result"""
    daily_trips: int
    peak_trips: Dict[str, int]
    los_impacts: List[IntersectionImpact]


class TransitStation(BaseModel):
    """Transit station information"""
    name: str
    line: str
    distance: float


class TransitAccess(BaseModel):
    """Transit access analysis result"""
    nearest_station: TransitStation
    walk_time_minutes: float
    transit_score: str
    nearby_stations: List[TransitStation]


class InfrastructureImpact(BaseModel):
    """Infrastructure capacity analysis result"""
    water_demand: float
    sewer_demand: float
    power_demand: float
    upgrades_needed: List[str]
    estimated_cost: float
    infrastructure_adequate: bool


class ShadowAnalysis(BaseModel):
    """Shadow analysis result"""
    shadows_by_time: List[Dict[str, Any]]
    total_affected_parcels: int


class EconomicImpact(BaseModel):
    """Economic impact analysis result"""
    annual_tax_revenue: float
    infrastructure_cost: float
    net_impact_year_1: float
    years_to_breakeven: float
    construction_jobs: int
    permanent_jobs: int


class Bottleneck(BaseModel):
    """Identified bottleneck/issue"""
    type: str
    severity: str
    message: str


class AIReport(BaseModel):
    """AI-generated report"""
    ai_summary: str
    timestamp: datetime


class BuildingAnalysisResponse(BaseModel):
    """Complete building analysis response"""
    building_id: str
    zoning: ZoningResult
    school_impact: SchoolImpact
    traffic_impact: TrafficImpact
    transit_access: TransitAccess
    infrastructure: InfrastructureImpact
    shadow_analysis: ShadowAnalysis
    economic_impact: EconomicImpact
    bottlenecks: List[Bottleneck]
    ai_report: AIReport
