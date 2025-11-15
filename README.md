# CityTrotter 🏙️

**City Development Impact Analyzer** - Real-time comprehensive analysis of urban development proposals

Built for Emory Hackathon | Smart City Track

## 🎯 Overview

CityTrotter is an integrated platform that provides instant, multi-domain impact analysis for proposed urban developments. Drop a building on a map, and get comprehensive insights across zoning, schools, traffic, transit, infrastructure, shadows, and economics - all enhanced by AI.

### The Problem
Current city planning tools are either expensive enterprise systems, limited academic tools, or fragmented open-source utilities. No accessible solution provides integrated, real-time development impact analysis.

### Our Solution
An interactive web platform where planners can:
- Place proposed developments on a map
- Get instant multi-domain impact analysis
- Visualize cascading effects
- Receive AI-enhanced recommendations
- Compare scenarios in real-time

## ✨ Features

- **🗺️ Interactive Mapping**: Mapbox-powered interface for Atlanta
- **📊 7-Domain Analysis**:
  - Zoning compliance
  - School capacity impact
  - Traffic generation (ITE standards)
  - Transit access (MARTA)
  - Infrastructure capacity
  - Shadow analysis
  - Economic impact
- **🤖 AI Enhancement**: Gemini-powered report generation
- **⚡ Real-time Results**: Analysis in 5-10 seconds
- **📈 Visual Dashboard**: Charts, metrics, and bottleneck alerts

## 🏗️ Tech Stack

### Frontend
- React 18 + Vite
- Mapbox GL JS (interactive maps)
- Recharts (data visualization)
- TailwindCSS (styling)
- Axios (API calls)

### Backend
- FastAPI (Python async framework)
- PostgreSQL + PostGIS (geospatial database)
- Google Gemini API (AI reports)
- Industry-standard formulas (ITE, EPA, HCM)

### Deployment
- Frontend: Vercel
- Backend: Railway/Render
- Database: Railway PostgreSQL + PostGIS

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL with PostGIS extension
- Mapbox account (free tier)
- Google Gemini API key (optional)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Set up environment variables
# Create .env file with:
# VITE_MAPBOX_TOKEN=your_mapbox_token
# VITE_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 📖 Usage

1. **Select Development Type**: Click "New Building" button
2. **Place on Map**: Click anywhere in Atlanta to set location
3. **Configure Building**:
   - Building type (residential/commercial/mixed-use)
   - Number of units
   - Number of stories
   - Parking spaces
4. **Analyze**: Click "Analyze Impact"
5. **Review Results**: See comprehensive analysis with:
   - Bottleneck alerts
   - Impact metrics
   - School capacity charts
   - Infrastructure requirements
   - Economic projections
   - AI-generated summary

## 📊 Analysis Details

### Industry Standards Used
- **Students per unit**: 0.3 (US Census Bureau avg)
- **Water demand**: 150 gpd/unit (EPA WaterSense)
- **Traffic generation**: ITE Trip Generation Manual Code 220
- **Property tax**: 1.1% (Atlanta/Fulton County rate)
- **Level of Service**: Highway Capacity Manual thresholds

### Mock Data (MVP)
For hackathon demo, using representative Atlanta data:
- 3 schools (Grady HS, Inman MS, Morningside ES)
- 3 MARTA stations (Arts Center, Midtown, North Avenue)
- Sample intersections for traffic analysis

Production version would use real GIS data from Atlanta Open Data Portal.

## 🎨 Project Structure

```
CityTrotter/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
├── data/             # Geospatial data
└── docs/             # Documentation
```

## 🌟 Key Differentiators

vs. Existing Tools:
- **ArcGIS Urban**: Expensive, enterprise-only → CityTrotter is free/accessible
- **UrbanSim**: Academic, narrow focus → We provide integrated analysis
- **Consultant reports**: Weeks, static → We deliver in seconds, interactive

## 🗺️ Roadmap

### MVP (Hackathon) ✅
- Building analysis with 7 domains
- AI-enhanced reports
- Visual dashboard
- Atlanta demo data

### Phase 2 (Post-Hackathon)
- Highway/infrastructure analysis
- Real Atlanta GIS data integration
- Scenario comparison
- PDF export

### Phase 3 (Future)
- Multiple cities (NYC, SF, Chicago)
- More development types
- ML timeline predictions
- Public participation features

## 👥 Target Users

- **City Planning Departments**: Development review
- **City Council Members**: Impact understanding
- **Community Groups**: Advocacy with data
- **Developers**: Pre-submission assessment

## 📝 License

MIT License (TBD)

## 🏆 Hackathon

- **Event**: Emory Hackathon
- **Track**: Smart City
- **Team**: Solo project by Yashas
- **Timeline**: 4 days

## 📧 Contact

**Project**: CityTrotter  
**GitHub**: https://github.com/RinneC0de/CityTrotter  
**Developer**: Yashas

## 🙏 Acknowledgments

- Industry standards: ITE, EPA, Highway Capacity Manual
- Data sources: Atlanta Open Data Portal, OpenStreetMap
- Technologies: Mapbox, Google Gemini, FastAPI, React

---

**Built with ❤️ for better cities**
