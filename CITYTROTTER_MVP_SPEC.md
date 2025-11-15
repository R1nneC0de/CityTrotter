# CityTrotter - MVP Specification

## Project Overview
**CityTrotter** is an integrated city development impact analyzer for the Emory Hackathon. It provides real-time analysis of proposed urban developments (buildings, highways, etc.) with comprehensive impact assessment.

**Target Track**: Smart City  
**Timeline**: 4-day hackathon  
**Demo Location**: Atlanta, GA  

---

## Problem Statement
Current city planning tools are either:
- Expensive enterprise GIS systems (ArcGIS Urban)
- Academic research tools (limited scope)
- Fragmented open-source utilities (single-purpose)

**Gap**: No accessible, integrated tool for comprehensive real-time development impact analysis.

---

## Solution
An interactive web platform where planners can:
1. Place proposed developments on a map
2. Get instant multi-domain impact analysis
3. Visualize cascading effects
4. Receive AI-enhanced recommendations
5. Compare scenarios in real-time

---

## MVP Scope (Hackathon Deliverable)

### **Primary Demo: Residential Building Analysis**
Focus on demonstrating comprehensive analysis with ONE development type done excellently.

**User Flow:**
1. User opens web app → sees Atlanta map
2. Clicks location → draws building footprint
3. Inputs: 300 units, 8 stories, 150 parking spaces
4. System analyzes (5-10 seconds)
5. Dashboard shows:
   - **Bottleneck alerts** (red warnings)
   - **Impact metrics** (school capacity, traffic, transit)
   - **Visual overlays** (impact zones, affected areas)
   - **3D shadow visualization**
   - **AI-generated summary report**
6. User can drag building → metrics update in real-time

### **Secondary Demo (Time Permitting): Highway Analysis**
Simpler analysis to show system flexibility:
- Traffic flow impact
- Community severance
- Alternative comparison (transit investment vs highway)

---

## Technical Architecture

### **Tech Stack**

#### Frontend
```
- React 18 + Vite
- Mapbox GL JS (interactive maps)
- Three.js (3D shadow visualization)
- Recharts (charts/graphs)
- TailwindCSS (styling)
- Axios (API calls)
```

#### Backend
```
- FastAPI (Python async framework)
- PostgreSQL + PostGIS (geospatial database)
- GeoPandas (geospatial operations)
- OSMnx (OpenStreetMap data)
- Shapely (geometric calculations)
- Google Gemini API (AI reports)
- Uvicorn (ASGI server)
```

#### Deployment
```
- Frontend: Vercel
- Backend: Railway or Render
- Database: Railway/Render PostgreSQL + PostGIS
- Version Control: GitHub
- CI/CD: GitHub Actions (optional)
```

---

## Core Analysis Functions (Backend)

### 1. **Zoning Compliance Check**
```python
Input: location (lat/lng), stories, units
Process:
  - Query PostGIS for zoning code at location
  - Check against Atlanta zoning rules (height, density, FAR)
  - Identify violations
Output: 
  {
    "zone": "MR-3",
    "compliant": true/false,
    "violations": ["list of violations"]
  }
```

### 2. **School Impact Analysis**
```python
Input: location, units
Process:
  - Calculate students: units × 0.3 (avg kids per unit)
  - Find schools within 1.5 mile radius (PostGIS)
  - Calculate new enrollment vs capacity by grade level
  - Identify bottlenecks (>100% capacity)
Output:
  {
    "students_generated": 90,
    "schools": [list of nearby schools with capacity data],
    "bottlenecks": [
      {"school": "Grady HS", "capacity_pct": 125, "severity": "HIGH"}
    ]
  }
```

### 3. **Traffic Impact Calculation**
```python
Input: units, location
Process:
  - Calculate daily trips: units × 9.57 (ITE Trip Generation Manual)
  - Calculate peak hour trips (11% AM, 12% PM)
  - Find intersections within 0.5 mile (OSM)
  - Calculate Level of Service (LOS) degradation
Output:
  {
    "daily_trips": 2871,
    "peak_trips": {"am": 316, "pm": 345},
    "los_impacts": [
      {"intersection": "10th & Peachtree", "current_los": "C", "projected_los": "F"}
    ]
  }
```

### 4. **Transit Access Analysis**
```python
Input: location
Process:
  - Find nearest MARTA stations (PostGIS)
  - Calculate walk time (distance / 1.4 m/s)
  - Calculate 10-min walk isochrone
  - Score: EXCELLENT (<5min), GOOD (<10min), FAIR (>10min)
Output:
  {
    "nearest_station": {"name": "Arts Center", "distance": 450},
    "walk_time_minutes": 5.4,
    "transit_score": "EXCELLENT"
  }
```

### 5. **Infrastructure Capacity Check**
```python
Input: units, location
Process:
  - Water demand: units × 150 gpd
  - Sewer demand: water × 0.8
  - Power demand: units × 2.5 kW
  - Query infrastructure data for water mains, sewer lines, substations
  - Check if capacity sufficient (70% threshold)
  - Estimate upgrade costs if needed
Output:
  {
    "water_demand": 45000,
    "infrastructure_adequate": false,
    "upgrades_needed": ["Water main upgrade required"],
    "estimated_cost": 850000
  }
```

### 6. **Shadow Analysis**
```python
Input: location, footprint polygon, stories
Process:
  - Building height: stories × 12 feet
  - Calculate sun positions for 9am, 12pm, 3pm, 5pm
  - Project shadow polygons based on sun angle
  - Find parcels/buildings intersecting shadows
  - Calculate shadow area and affected properties
Output:
  {
    "shadows_by_time": [
      {"time": "9:00 AM", "shadow_area_sqft": 12000, "affected_parcels": 5}
    ],
    "total_affected_parcels": 8
  }
```

### 7. **Economic Impact**
```python
Input: units, stories, infrastructure_cost
Process:
  - Estimate property value: units × avg_rent × 12 × 20
  - Annual tax revenue: value × 1.1% (Atlanta rate)
  - Construction jobs: (units × stories) / 2
  - Permanent jobs: units / 50
  - Break-even: infrastructure_cost / annual_tax_revenue
Output:
  {
    "annual_tax_revenue": 132000,
    "infrastructure_cost": 850000,
    "years_to_breakeven": 6.4,
    "construction_jobs": 1200,
    "permanent_jobs": 6
  }
```

### 8. **AI Report Generation (Gemini)**
```python
Input: all analysis results
Process:
  - Format structured prompt with all metrics
  - Send to Gemini API
  - Request: executive summary, critical issues, recommendations, timeline
Output:
  {
    "ai_summary": "markdown formatted report",
    "timestamp": "2025-11-15T10:30:00Z"
  }
```

---

## Data Sources

### Required for MVP
1. **Atlanta Zoning Data**: GeoJSON polygons with zoning codes
2. **Atlanta Public Schools**: Locations, enrollment, capacity
3. **MARTA Stations**: Transit network data
4. **OpenStreetMap**: Buildings, roads, intersections (via OSMnx)
5. **Census Data**: Demographics (optional for enhanced analysis)

### Data Acquisition
```python
# OSM data (free, API)
import osmnx as ox
buildings = ox.geometries_from_place("Atlanta, Georgia", tags={'building': True})
roads = ox.graph_from_place("Atlanta, Georgia", network_type='drive')

# Atlanta Open Data Portal
# https://gis.atlantaga.gov/
# Download: zoning.geojson, schools.geojson, infrastructure.geojson
```

---

## Frontend Components

### **1. Map.jsx**
- Mapbox GL JS integration
- Click handler for building placement
- Drawing tools for footprint
- Layer toggles (zoning, schools, transit)
- Impact zone overlays (colored circles)
- Marker popups with data

### **2. BuildingPlacer.jsx**
- Form inputs: units, stories, parking
- Submit button → triggers analysis
- Loading state during backend processing
- Clear/reset functionality

### **3. ImpactDashboard.jsx**
- Bottleneck alerts (red/yellow/green)
- Metric cards (school, traffic, transit, economic)
- Charts: school capacity bar chart, traffic impact
- AI summary section
- Export/share buttons

### **4. ShadowViz.jsx**
- Three.js 3D building rendering
- Shadow projection visualization
- Time slider (9am → 5pm)
- Affected parcels highlighted

### **5. ScenarioComparison.jsx** (stretch goal)
- Side-by-side comparison table
- Save/load scenarios
- Difference highlighting

---

## API Endpoints

### **POST /api/v1/analyze-building**
```json
Request:
{
  "location": {"lat": 33.7756, "lng": -84.3963},
  "footprint": [[lng1, lat1], [lng2, lat2], [lng3, lat3], [lng4, lat4]],
  "type": "residential",
  "units": 300,
  "stories": 8,
  "parking_spaces": 150
}

Response:
{
  "building_id": "uuid",
  "zoning": {...},
  "school_impact": {...},
  "traffic_impact": {...},
  "transit_access": {...},
  "infrastructure": {...},
  "shadow_analysis": {...},
  "economic_impact": {...},
  "bottlenecks": [...],
  "ai_report": {...}
}
```

### **GET /api/v1/data/schools**
Get all schools in Atlanta (for map layer)

### **GET /api/v1/data/zoning**
Get zoning boundaries (for map layer)

### **GET /api/v1/data/marta-stations**
Get MARTA station locations (for map layer)

### **POST /api/v1/analyze-highway** (stretch)
Similar to building analysis, different calculations

---

## Project Structure

```
CityTrotter/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map.jsx
│   │   │   ├── BuildingPlacer.jsx
│   │   │   ├── ImpactDashboard.jsx
│   │   │   ├── ShadowViz.jsx
│   │   │   └── AlertBanner.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── utils/
│   │   │   └── helpers.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── building.py
│   │   │   └── analysis.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── building_analysis.py
│   │   │   ├── data.py
│   │   │   └── highway_analysis.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── zoning_checker.py
│   │   │   ├── school_analyzer.py
│   │   │   ├── traffic_calculator.py
│   │   │   ├── transit_analyzer.py
│   │   │   ├── infrastructure_analyzer.py
│   │   │   ├── shadow_calculator.py
│   │   │   ├── economic_analyzer.py
│   │   │   ├── gemini_service.py
│   │   │   └── osm_fetcher.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── geo_utils.py
│   │       └── constants.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── data/
│   ├── atlanta_zoning.geojson
│   ├── atlanta_schools.geojson
│   ├── marta_stations.geojson
│   └── README.md
│
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEMO_SCRIPT.md
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── .gitignore
├── README.md
├── docker-compose.yml
└── CITYTROTTER_MVP_SPEC.md (this file)
```

---

## Database Schema

### **buildings** table
```sql
CREATE TABLE buildings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location GEOGRAPHY(POINT, 4326),
    footprint GEOGRAPHY(POLYGON, 4326),
    type VARCHAR(50),
    units INTEGER,
    stories INTEGER,
    parking_spaces INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **analyses** table
```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    building_id UUID REFERENCES buildings(id),
    zoning_data JSONB,
    school_impact JSONB,
    traffic_impact JSONB,
    transit_access JSONB,
    infrastructure JSONB,
    shadow_analysis JSONB,
    economic_impact JSONB,
    bottlenecks JSONB,
    ai_report JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **schools** table (pre-populated)
```sql
CREATE TABLE schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    geom GEOGRAPHY(POINT, 4326),
    grade_level VARCHAR(50),
    enrollment INTEGER,
    capacity INTEGER
);
```

### **zoning_zones** table (pre-populated)
```sql
CREATE TABLE zoning_zones (
    id SERIAL PRIMARY KEY,
    zone_code VARCHAR(20),
    geom GEOGRAPHY(POLYGON, 4326),
    max_height INTEGER,
    max_far DECIMAL,
    max_units_per_acre INTEGER
);
```

---

## Environment Variables

### Frontend (.env)
```
VITE_MAPBOX_TOKEN=your_mapbox_token
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/citytrotter
GEMINI_API_KEY=your_gemini_api_key
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173
```

---

## 4-Day Implementation Timeline

### **Day 1: Foundation (8 hours)**
**Morning (4h):**
- ✅ Initialize Git repo
- ✅ Set up frontend: React + Vite + TailwindCSS
- ✅ Set up backend: FastAPI + basic structure
- ✅ Set up PostgreSQL + PostGIS locally
- ✅ Configure environment variables
- ✅ Create basic Mapbox map component

**Afternoon (4h):**
- ✅ Implement map click → place marker
- ✅ Create BuildingPlacer form UI
- ✅ Set up API endpoint structure
- ✅ Test frontend → backend → database connection
- ✅ Download/prepare Atlanta data (zoning, schools, MARTA)

### **Day 2: Core Analysis (8-10 hours)**
**Morning (5h):**
- ✅ Implement zoning check function
- ✅ Implement school impact calculation
- ✅ Implement traffic impact calculation
- ✅ Implement transit access analysis
- ✅ Test each function independently

**Afternoon (4h):**
- ✅ Implement infrastructure capacity check
- ✅ Implement shadow analysis (basic version)
- ✅ Implement economic impact calculation
- ✅ Integrate Gemini API for report generation
- ✅ Wire all functions to main analysis endpoint

### **Day 3: Frontend + Polish (8-10 hours)**
**Morning (4h):**
- ✅ Build ImpactDashboard component
- ✅ Create visualizations (charts, metrics)
- ✅ Add map overlays (impact zones, markers)
- ✅ Implement bottleneck alerts UI
- ✅ Display AI summary

**Afternoon (4h):**
- ✅ Implement Three.js shadow visualization
- ✅ Add real-time updates (drag building feature)
- ✅ UI/UX polish (styling, animations)
- ✅ Test full workflow end-to-end
- ✅ Bug fixes

**Evening (2h - optional):**
- ✅ Start highway demo (basic implementation)

### **Day 4: Deployment + Demo Prep (6-8 hours)**
**Morning (4h):**
- ✅ Deploy backend to Railway/Render
- ✅ Deploy frontend to Vercel
- ✅ Configure production environment variables
- ✅ Test production deployment
- ✅ Load production data

**Afternoon (3h):**
- ✅ Create demo video/screenshots
- ✅ Write comprehensive README
- ✅ Prepare pitch deck (problem, solution, demo)
- ✅ Practice demo presentation (7 minutes)
- ✅ Final testing and polish

---

## Demo Script (7 minutes)

### **Opening (1 min)**
"City planners spend weeks analyzing development proposals. CityTrotter does it in seconds. Watch."

### **Demo - Building Analysis (4 min)**
1. "Let's propose a 300-unit apartment building in Midtown Atlanta"
2. *Click map, draw footprint, fill form*
3. *Click Analyze*
4. "In 5 seconds, we get comprehensive impact analysis across 7 domains"
5. **Show bottleneck alerts**: "Grady High School will be at 125% capacity - major issue"
6. **Show traffic**: "3 intersections degraded to Level F"
7. **Show transit**: "Excellent - 5 minute walk to MARTA Arts Center"
8. **Show shadow viz**: "Here's the 3D shadow impact at different times"
9. **Show AI summary**: "Gemini predicts 18-month permitting with community opposition"
10. **Drag building**: "Watch metrics update in real-time as I move it 3 blocks east"
11. "School impact drops 60%, but transit access worsens - clear trade-offs"

### **Quick Highway Demo (1 min)** (if time permits)
"Same analysis works for infrastructure. New highway divides neighborhoods - but here's the transit alternative"

### **Closing (1 min)**
"CityTrotter makes planning:
- **Faster**: Weeks → Seconds
- **Transparent**: All impacts visible
- **Data-driven**: Real calculations + AI insights
- **Accessible**: Free, open-source potential

**Impact**: Helps city planners, council members, community groups, and developers make better decisions together."

---

## Success Criteria

### **Must Have (MVP)**
- ✅ Interactive map with building placement
- ✅ At least 5 analysis functions working (zoning, school, traffic, transit, infrastructure)
- ✅ Visual dashboard with metrics and charts
- ✅ AI-generated summary report
- ✅ Deployed and accessible via public URL
- ✅ Working demo (building analysis)

### **Should Have**
- ✅ Shadow visualization (Three.js)
- ✅ Real-time updates when dragging building
- ✅ All 7 analysis functions
- ✅ Bottleneck identification and alerts
- ✅ Economic impact analysis

### **Nice to Have**
- ⭕ Highway demo (secondary)
- ⭕ Scenario comparison
- ⭕ PDF export
- ⭕ Public sharing links
- ⭕ Historical timeline prediction (ML)

---

## Key Differentiators

### **vs. Existing Tools:**
1. **ArcGIS Urban**: Expensive ($$$), complex, enterprise-only
2. **UrbanSim**: Academic, narrow focus
3. **Open source GIS**: Fragmented, single-purpose
4. **Consultant reports**: Slow (weeks), expensive, static

### **CityTrotter Advantages:**
- ✅ **Integrated**: Multiple domains in one analysis
- ✅ **Fast**: Real-time results
- ✅ **Accessible**: Web-based, no GIS expertise required
- ✅ **Interactive**: Drag-and-drop, instant updates
- ✅ **AI-Enhanced**: Smart insights, not just data
- ✅ **Open**: Can be open-sourced, free for cities

---

## Risk Mitigation

### **Technical Risks:**
1. **PostGIS setup complexity**: Use Railway/Render managed PostgreSQL
2. **Data availability**: Pre-download Atlanta data, cache locally
3. **API rate limits**: Cache Gemini responses, use free tier wisely
4. **Performance**: Simplify calculations if needed, optimize queries

### **Scope Risks:**
1. **Too ambitious**: Focus on building demo first, highway is optional
2. **Time constraints**: Cut nice-to-haves, prioritize core analysis
3. **Demo failure**: Pre-record backup video, test extensively

### **Deployment Risks:**
1. **Last-minute bugs**: Deploy by end of Day 3, Day 4 for fixes
2. **Environment issues**: Test production deployment early
3. **Data loading**: Pre-populate database, don't rely on live fetching

---

## Post-Hackathon Potential

### **Immediate Extensions:**
- Add more cities (NYC, SF, Chicago)
- More development types (parks, industrial, mixed-use)
- Historical permitting timeline ML model
- Public participation features (community feedback)

### **Long-term Vision:**
- SaaS for city planning departments
- Open-source core + enterprise features
- API for third-party integrations
- Mobile app for field use

### **Business Model:**
- **Free tier**: Basic analysis, limited cities
- **Pro tier**: Advanced features, unlimited analysis, API access
- **Enterprise**: Custom deployment, training, support
- **Grant funding**: National Science Foundation, urban planning associations

---

## Technical Notes

### **Optimization Tips:**
```python
# Use spatial indexes in PostGIS
CREATE INDEX idx_schools_geom ON schools USING GIST(geom);
CREATE INDEX idx_zoning_geom ON zoning_zones USING GIST(geom);

# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=100)
def get_schools_in_radius(lat, lng, radius):
    # Expensive query cached
    pass

# Async processing for parallel analysis
import asyncio

async def analyze_building(building):
    results = await asyncio.gather(
        check_zoning(building),
        analyze_schools(building),
        calculate_traffic(building),
        # ... all functions run in parallel
    )
    return combine_results(results)
```

### **Frontend Performance:**
```javascript
// Debounce drag updates
import { debounce } from 'lodash';

const debouncedAnalysis = debounce(async (location) => {
  const results = await api.quickAnalyze(location);
  updateDashboard(results);
}, 500);

// Lazy load Three.js
const ShadowViz = lazy(() => import('./ShadowViz'));
```

---

## Resources & References

### **Documentation:**
- Mapbox GL JS: https://docs.mapbox.com/mapbox-gl-js/
- PostGIS: https://postgis.net/documentation/
- FastAPI: https://fastapi.tiangolo.com/
- OSMnx: https://osmnx.readthedocs.io/
- Gemini API: https://ai.google.dev/docs

### **Data Sources:**
- Atlanta Open Data: https://gis.atlantaga.gov/
- OpenStreetMap: https://www.openstreetmap.org/
- Census Bureau: https://data.census.gov/
- ITE Trip Generation: Industry standard formulas

### **Tutorials:**
- PostGIS tutorial: https://postgis.net/workshops/postgis-intro/
- Mapbox React integration: https://docs.mapbox.com/help/tutorials/use-mapbox-gl-js-with-react/
- Three.js basics: https://threejs.org/docs/index.html#manual/en/introduction/Creating-a-scene

---

## Contact & Team

**Project**: CityTrotter  
**Hackathon**: Emory Hackathon  
**Track**: Smart City  
**Developer**: Yashas  
**GitHub**: https://github.com/yourusername/CityTrotter  

---

## License
MIT License (to be added)

---

**Last Updated**: November 15, 2025  
**Version**: 1.0 (MVP Specification)

---

## Quick Start Commands

### **Local Development Setup:**
```bash
# Clone repo
git clone https://github.com/yourusername/CityTrotter.git
cd CityTrotter

# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup (in new terminal)
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Database setup
# Install PostgreSQL + PostGIS
# Create database: createdb citytrotter
# Enable PostGIS: psql -d citytrotter -c "CREATE EXTENSION postgis;"
# Run migrations (TBD)
```

### **Deployment:**
```bash
# Frontend (Vercel)
cd frontend
vercel --prod

# Backend (Railway)
railway login
railway up
railway add --plugin postgresql

# Set environment variables in Railway dashboard
```

---

## End of MVP Specification

**This document contains all context needed to build CityTrotter MVP.**
Use this as reference throughout development.
