import { useState } from 'react'
import { analyzeBuilding } from '../services/api'

function BuildingPlacer({ selectedLocation, onAnalysisStart, onAnalysisComplete }) {
  const [formData, setFormData] = useState({
    type: 'residential',
    units: 300,
    stories: 8,
    parkingSpaces: 150
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'type' ? value : parseInt(value) || 0
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!selectedLocation) {
      alert('Please select a location on the map first')
      return
    }

    onAnalysisStart()

    try {
      // Create a simple rectangular footprint around the selected point
      // In production, this would be drawn by the user
      const offset = 0.001 // ~100m offset
      const footprint = [
        [selectedLocation.lng - offset, selectedLocation.lat - offset],
        [selectedLocation.lng + offset, selectedLocation.lat - offset],
        [selectedLocation.lng + offset, selectedLocation.lat + offset],
        [selectedLocation.lng - offset, selectedLocation.lat + offset],
        [selectedLocation.lng - offset, selectedLocation.lat - offset]
      ]

      const buildingData = {
        location: selectedLocation,
        footprint: footprint,
        type: formData.type,
        units: formData.units,
        stories: formData.stories,
        parking_spaces: formData.parkingSpaces
      }

      const results = await analyzeBuilding(buildingData)
      onAnalysisComplete(results)
    } catch (error) {
      console.error('Analysis failed:', error)
      alert('Analysis failed. Please check console for details.')
      onAnalysisComplete(null)
    }
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Building Details</h2>

      {!selectedLocation && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-yellow-800">
            👆 Click on the map to select a location first
          </p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Building Type
          </label>
          <select
            name="type"
            value={formData.type}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="residential">Residential</option>
            <option value="commercial">Commercial</option>
            <option value="mixed-use">Mixed-Use</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Units
          </label>
          <input
            type="number"
            name="units"
            value={formData.units}
            onChange={handleChange}
            min="1"
            max="1000"
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 mt-1">
            Recommended: 50-500 units
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Stories
          </label>
          <input
            type="range"
            name="stories"
            value={formData.stories}
            onChange={handleChange}
            min="1"
            max="20"
            className="w-full"
          />
          <div className="flex justify-between text-sm text-gray-600">
            <span>1</span>
            <span className="font-bold text-blue-600">{formData.stories} stories ({formData.stories * 12} ft)</span>
            <span>20</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Parking Spaces
          </label>
          <input
            type="number"
            name="parkingSpaces"
            value={formData.parkingSpaces}
            onChange={handleChange}
            min="0"
            max="1000"
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 mt-1">
            Typical: 0.5-2 spaces per unit
          </p>
        </div>

        <button
          type="submit"
          disabled={!selectedLocation}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition"
        >
          Analyze Impact
        </button>
      </form>

      {selectedLocation && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm font-medium text-gray-700 mb-2">Selected Location:</p>
          <p className="text-xs text-gray-600 font-mono">
            {selectedLocation.lat.toFixed(4)}, {selectedLocation.lng.toFixed(4)}
          </p>
        </div>
      )}
    </div>
  )
}

export default BuildingPlacer
