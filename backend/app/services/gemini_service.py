"""
Gemini AI service for generating planning reports
"""

from app.models.analysis import AIReport
from app.config import settings
from datetime import datetime
import os


async def generate_planning_report(analysis_data: dict) -> AIReport:
    """
    Generate AI-enhanced planning report using Google Gemini
    
    Args:
        analysis_data: Complete analysis results
    
    Returns:
        AIReport with AI-generated summary
    """
    
    # Check if Gemini API key is configured
    if not settings.GEMINI_API_KEY:
        # Return a template report if no API key
        return AIReport(
            ai_summary=generate_template_report(analysis_data),
            timestamp=datetime.now()
        )
    
    try:
        # Import here to avoid dependency issues if not using Gemini
        import google.generativeai as genai
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = create_analysis_prompt(analysis_data)
        
        response = model.generate_content(prompt)
        
        return AIReport(
            ai_summary=response.text,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        # Fallback to template if API fails
        print(f"Gemini API error: {str(e)}")
        return AIReport(
            ai_summary=generate_template_report(analysis_data),
            timestamp=datetime.now()
        )


def create_analysis_prompt(data: dict) -> str:
    """
    Create structured prompt for Gemini
    """
    building = data["building"]
    zoning = data["zoning"]
    school = data["school_impact"]
    traffic = data["traffic_impact"]
    transit = data["transit_access"]
    infra = data["infrastructure"]
    economic = data["economic_impact"]
    
    prompt = f"""You are an expert city planner analyzing a proposed development. Generate a concise impact report.

PROPOSED DEVELOPMENT:
- Location: Atlanta, GA ({building["location"]["lat"]}, {building["location"]["lng"]})
- Type: {building["type"].title()}
- Size: {building["units"]} units, {building["stories"]} stories
- Parking: {building["parking_spaces"]} spaces

ANALYSIS RESULTS:

Zoning: {"✓ Compliant" if zoning.compliant else "✗ Violations: " + ", ".join(zoning.violations)}
Zone: {zoning.zone}

School Impact:
- New students: {school.students_generated:.0f}
- Bottlenecks: {len(school.bottlenecks)} schools overcapacity
{format_school_bottlenecks(school.bottlenecks)}

Traffic Impact:
- Daily trips: {traffic.daily_trips:,}
- Peak hour trips: AM {traffic.peak_trips["am"]}, PM {traffic.peak_trips["pm"]}
- Degraded intersections: {len(traffic.los_impacts)}

Transit Access: {transit.transit_score}
- Nearest station: {transit.nearest_station.name} ({transit.walk_time_minutes:.1f} min walk)

Infrastructure: {"Adequate" if infra.infrastructure_adequate else "Upgrades needed"}
- Water demand: {infra.water_demand:,.0f} gpd
- Upgrades needed: {", ".join(infra.upgrades_needed) if infra.upgrades_needed else "None"}
- Cost: ${infra.estimated_cost:,.0f}

Economics:
- Annual tax revenue: ${economic.annual_tax_revenue:,.0f}
- Infrastructure cost: ${economic.infrastructure_cost:,.0f}
- Break-even: {economic.years_to_breakeven:.1f} years
- Jobs: {economic.construction_jobs} construction, {economic.permanent_jobs} permanent

Provide:
1. **Executive Summary** (2-3 sentences highlighting key findings)
2. **Critical Issues** (top 3 concerns with severity)
3. **Recommendations** (3 specific, actionable suggestions to mitigate impacts)
4. **Timeline Estimate** (permitting duration based on complexity and likely opposition)

Keep it professional but concise. Use bullet points for clarity.
"""
    
    return prompt


def format_school_bottlenecks(bottlenecks: list) -> str:
    """Format school bottlenecks for prompt"""
    if not bottlenecks:
        return "- None"
    
    lines = []
    for b in bottlenecks[:3]:  # Top 3
        lines.append(f"  - {b['school']}: {b['capacity_pct']:.0f}% capacity ({b['severity']})")
    return "\n".join(lines)


def generate_template_report(data: dict) -> str:
    """
    Generate template report when Gemini is unavailable
    """
    building = data["building"]
    bottlenecks = []
    
    if not data["zoning"].compliant:
        bottlenecks.append("Zoning compliance issues")
    if data["school_impact"].bottlenecks:
        bottlenecks.append(f"{len(data['school_impact'].bottlenecks)} schools over capacity")
    if data["traffic_impact"].los_impacts:
        bottlenecks.append("Traffic congestion at nearby intersections")
    if not data["infrastructure"].infrastructure_adequate:
        bottlenecks.append("Infrastructure upgrades required")
    
    report = f"""**Executive Summary**

The proposed {building["units"]}-unit residential development presents {"several challenges" if bottlenecks else "a viable opportunity"} for the community. {"Key concerns include: " + ", ".join(bottlenecks) + "." if bottlenecks else "Analysis shows generally positive impacts with manageable constraints."}

**Critical Issues**

{"1. " + bottlenecks[0] if len(bottlenecks) > 0 else "1. No major issues identified"}
{"2. " + bottlenecks[1] if len(bottlenecks) > 1 else "2. Minor infrastructure considerations"}
{"3. " + bottlenecks[2] if len(bottlenecks) > 2 else "3. Standard permitting requirements"}

**Recommendations**

1. Conduct detailed traffic impact study for affected intersections
2. Coordinate with school district on capacity planning
3. {"Secure funding for infrastructure upgrades" if data["infrastructure"].infrastructure_adequate == False else "Verify utility connections with service providers"}

**Timeline Estimate**

Based on project complexity and identified impacts, expect {"18-24 months" if len(bottlenecks) > 2 else "12-18 months" if len(bottlenecks) > 0 else "9-12 months"} for permitting and approval process.

*Note: This is an automated analysis. Detailed engineering studies recommended.*
"""
    
    return report
