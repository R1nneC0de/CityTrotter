import { useState } from 'react'

function BuildingPlacer({ selectedLocation, onAnalysisStart, onStoriesChange, onBuildingDataChange }) {
  const [formData, setFormData] = useState({
    type: 'residential',
    units: 300,
    stories: 8,
    parkingSpaces: 150,
    footprintArea: 2500
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    const newValue = name === 'type' ? value : parseInt(value) || 0
    
    const newFormData = {
      ...formData,
      [name]: newValue
    }
    
    setFormData(newFormData)
    
    // Notify parent of changes
    if (onBuildingDataChange) {
      onBuildingDataChange(newFormData)
    }
    
    if (name === 'stories' && onStoriesChange) {
      onStoriesChange(newValue)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!selectedLocation) {
      alert('Please select a location on the map first')
      return
    }

    // Pass form data to parent
    onAnalysisStart(formData)
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
      {/* Building Type */}
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

      {/* Number of Units */}
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

      {/* Number of Stories */}
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

      {/* Building Footprint Area - ONLY ONE! */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Building Footprint Area (sq ft)
        </label>
        <input
          type="range"
          name="footprintArea"
          value={formData.footprintArea}
          onChange={handleChange}
          min="800"
          max="8000"
          step="100"
          className="w-full"
        />
        <div className="flex justify-between text-sm text-gray-600">
          <span>800 ft²</span>
          <span className="font-bold text-blue-600">
            {formData.footprintArea.toLocaleString()} ft² 
            ({Math.sqrt(formData.footprintArea).toFixed(0)} × {Math.sqrt(formData.footprintArea).toFixed(0)} ft)
          </span>
          <span>8,000 ft²</span>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Small: 800-2,000 ft² | Medium: 2,500-5,000 ft² | Large: 5,000-8,000 ft²
        </p>
      </div>

      {/* Parking Spaces */}
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

      {/* Analyze Button */}
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