import { useState, useRef } from 'react'
import Map from './components/Map'
import BuildingPlacer from './components/BuildingPlacer'
import ImpactDashboard from './components/ImpactDashboard'
import { analyzeBuilding } from './services/api'
import './App.css'

function App() {
  const [selectedLocation, setSelectedLocation] = useState(null)
  const [buildingFootprint, setBuildingFootprint] = useState(null)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [mode, setMode] = useState(null)
  const [buildingStories, setBuildingStories] = useState(8)
  const [buildingArea, setBuildingArea] = useState(1500) // ✅ NEW: Track building area
  
  // Store building data for re-analysis
  const [buildingData, setBuildingData] = useState({
    type: 'residential',
    units: 300,
    stories: 8,
    parkingSpaces: 150,
    footprintArea: 2500 // ✅ NEW: Default area
  })

  // Use ref to track if we have analysis results (more reliable than state for timing)
  const hasAnalyzedRef = useRef(false)
  const reanalyzeTimerRef = useRef(null) // ✅ NEW: Timer for debounced re-analysis

  const handleLocationSelect = (location) => {
    setSelectedLocation(location)
  }

  const handleLocationChange = async (newLocation) => {
    console.log('🔵 handleLocationChange called with:', newLocation)
    console.log('🔵 hasAnalyzedRef.current:', hasAnalyzedRef.current)
    console.log('🔵 Current buildingData:', buildingData)
    
    // Update location
    setSelectedLocation(newLocation)
    
    // Auto-trigger analysis if we already have results
    if (hasAnalyzedRef.current) {
      console.log('✅ Auto-reanalyzing at new location:', newLocation)
      await performAnalysis(newLocation, buildingData)
    } else {
      console.log('❌ No analysis yet, skipping re-analysis')
    }
  }

  const performAnalysis = async (location, formData) => {
    if (!location) {
      alert('Please select a location on the map first')
      return
    }
  
    console.log('🟡 Starting analysis...')
    setIsAnalyzing(true)
  
    try {
      // ✅ UPDATED: Use dynamic footprint area
      const sideLengthFeet = Math.sqrt(formData.footprintArea)
      const sideLengthDegrees = sideLengthFeet / 305000
      const offset = sideLengthDegrees / 2
      
      const footprint = [
        [location.lng - offset, location.lat - offset],
        [location.lng + offset, location.lat - offset],
        [location.lng + offset, location.lat + offset],
        [location.lng - offset, location.lat + offset],
        [location.lng - offset, location.lat - offset]
      ]
  
      const analysisData = {
        location: location,
        footprint: footprint,
        type: formData.type,
        units: formData.units,
        stories: formData.stories,
        parking_spaces: formData.parkingSpaces
      }
  
      console.log('Sending analysis request:', analysisData)
      const results = await analyzeBuilding(analysisData)
      console.log('Analysis complete:', results)
      
      console.log('🟢 Setting analysisResults state...')
      setAnalysisResults(results)
      hasAnalyzedRef.current = true
      console.log('🟢 hasAnalyzedRef set to true')
      setIsAnalyzing(false)
    } catch (error) {
      console.error('Analysis failed:', error)
      alert('Analysis failed. Please check console for details.')
      setIsAnalyzing(false)
    }
  }

  const handleFootprintComplete = (footprint) => {
    setBuildingFootprint(footprint)
  }

  const handleAnalysisStart = (formData) => {
    // Store the building data for future re-analysis
    setBuildingData(formData)
    performAnalysis(selectedLocation, formData)
  }

  const handleReset = () => {
    setSelectedLocation(null)
    setBuildingFootprint(null)
    setAnalysisResults(null)
    setMode(null)
    setIsAnalyzing(false)
    hasAnalyzedRef.current = false
    setBuildingStories(8) // ✅ Reset stories
    setBuildingArea(2500) // ✅ Reset area
    setBuildingData({
      type: 'residential',
      units: 300,
      stories: 8,
      parkingSpaces: 150,
      footprintArea: 2500 // ✅ Reset area
    })
  }

  const handleBuildingDataChange = (newData) => {
    console.log('🔄 Building data changed:', newData)
    setBuildingData(newData)
    
    // ✅ Update stories for 3D building
    if (newData.stories !== undefined) {
      setBuildingStories(newData.stories)
    }
    
    // ✅ Update area for 3D building
    if (newData.footprintArea !== undefined) {
      setBuildingArea(newData.footprintArea)
    }
    
    // ✅ AUTO RE-ANALYSIS: If we already analyzed, re-analyze after 1.5 seconds
    if (hasAnalyzedRef.current && selectedLocation) {
      console.log('🟡 Building parameters changed, scheduling re-analysis...')
      
      // Clear existing timer
      if (reanalyzeTimerRef.current) {
        clearTimeout(reanalyzeTimerRef.current)
      }
      
      // Set new timer
      reanalyzeTimerRef.current = setTimeout(() => {
        console.log('✅ Auto-reanalyzing with new building parameters')
        performAnalysis(selectedLocation, newData)
      }, 1500) // Wait 1.5 seconds after user stops changing sliders
    }
  }

  return (
    <div className="w-screen h-screen flex flex-col">
      {/* Header */}
      <header className="bg-gray-900 text-white py-4 px-6 shadow-lg z-10">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">CityTrotter</h1>
            <p className="text-sm text-gray-300">City Development Impact Analyzer</p>
          </div>
          
          {!mode && (
            <div className="flex gap-4">
              <button
                onClick={() => setMode('building')}
                className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-medium transition"
              >
                New Building
              </button>
              <button
                onClick={() => setMode('highway')}
                className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded-lg font-medium transition"
                disabled
                title="Coming soon"
              >
                Highway Project
              </button>
            </div>
          )}
          
          {mode && (
            <button
              onClick={handleReset}
              className="bg-red-600 hover:bg-red-700 px-6 py-2 rounded-lg font-medium transition"
            >
              Reset
            </button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Map Section */}
        <div className="flex-1 relative">
          <Map
            selectedLocation={selectedLocation}
            buildingFootprint={buildingFootprint}
            analysisResults={analysisResults}
            onLocationSelect={handleLocationSelect}
            onLocationChange={handleLocationChange}
            onFootprintComplete={handleFootprintComplete}
            mode={mode}
            buildingStories={buildingStories}
            buildingArea={buildingArea} // ✅ NEW: Pass building area to map
          />
          
          {isAnalyzing && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-8 text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                <p className="text-lg font-medium">
                  {analysisResults ? 'Re-analyzing...' : 'Analyzing development impact...'}
                </p>
                <p className="text-sm text-gray-500 mt-2">This may take 5-10 seconds</p>
              </div>
            </div>
          )}
        </div>

        {/* Side Panel - ALWAYS SHOW when in building mode */}
        {mode === 'building' && (
          <div className="w-96 bg-white border-l border-gray-200 overflow-y-auto">
            <BuildingPlacer
              selectedLocation={selectedLocation}
              buildingFootprint={buildingFootprint}
              onAnalysisStart={handleAnalysisStart}
              onStoriesChange={setBuildingStories}
              onBuildingDataChange={handleBuildingDataChange}
              hasResults={hasAnalyzedRef.current} // ✅ NEW: Tell form if we have results
            />
          </div>
        )}

        {/* Results Dashboard */}
        {analysisResults && (
          <div className="w-1/2 bg-white border-l border-gray-200 overflow-y-auto">
            <ImpactDashboard results={analysisResults} />
            
            {/* Updated hint */}
            <div className="p-4 bg-blue-50 border-t border-blue-100">
              <p className="text-sm text-blue-800 mb-2">
                💡 <strong>Tips:</strong>
              </p>
              <ul className="text-xs text-blue-700 space-y-1">
                <li>🖱️ Drag the marker to test different locations</li>
                <li>🎚️ Adjust building parameters on the left</li>
                <li>⚡ Analysis updates automatically after changes</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App