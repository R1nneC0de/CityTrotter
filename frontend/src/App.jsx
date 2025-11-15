import { useState } from 'react'
import Map from './components/Map'
import BuildingPlacer from './components/BuildingPlacer'
import ImpactDashboard from './components/ImpactDashboard'
import './App.css'

function App() {
  const [selectedLocation, setSelectedLocation] = useState(null)
  const [buildingFootprint, setBuildingFootprint] = useState(null)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [mode, setMode] = useState(null) // null, 'building', 'highway'

  const handleLocationSelect = (location) => {
    setSelectedLocation(location)
  }

  const handleFootprintComplete = (footprint) => {
    setBuildingFootprint(footprint)
  }

  const handleAnalysisComplete = (results) => {
    setAnalysisResults(results)
    setIsAnalyzing(false)
  }

  const handleAnalysisStart = () => {
    setIsAnalyzing(true)
  }

  const handleReset = () => {
    setSelectedLocation(null)
    setBuildingFootprint(null)
    setAnalysisResults(null)
    setMode(null)
  }

  const [buildingStories, setBuildingStories] = useState(8) // Add this state


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
            onFootprintComplete={handleFootprintComplete}
            mode={mode}
            buildingStories={buildingStories}
          />
          
          {isAnalyzing && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-8 text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                <p className="text-lg font-medium">Analyzing development impact...</p>
                <p className="text-sm text-gray-500 mt-2">This may take 5-10 seconds</p>
              </div>
            </div>
          )}
        </div>

        {/* Side Panel */}
        {mode === 'building' && !analysisResults && (
          <div className="w-96 bg-white border-l border-gray-200 overflow-y-auto">
            <BuildingPlacer
              selectedLocation={selectedLocation}
              buildingFootprint={buildingFootprint}
              onAnalysisStart={handleAnalysisStart}
              onAnalysisComplete={handleAnalysisComplete}
              onStoriesChange={setBuildingStories}
            />
          </div>
        )}

        {/* Results Dashboard */}
        {analysisResults && (
          <div className="w-1/2 bg-white border-l border-gray-200 overflow-y-auto">
            <ImpactDashboard results={analysisResults} />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
