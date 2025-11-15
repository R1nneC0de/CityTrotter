import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'

// Set your Mapbox token
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.YOUR_MAPBOX_TOKEN_HERE'

function Map({ selectedLocation, buildingFootprint, analysisResults, onLocationSelect, mode }) {
  const mapContainer = useRef(null)
  const map = useRef(null)
  const marker = useRef(null)

  useEffect(() => {
    if (map.current) return // Initialize map only once

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-84.3880, 33.7490], // Atlanta, GA
      zoom: 13
    })

    // Add navigation controls
    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right')

    // Handle map clicks
    map.current.on('click', (e) => {
      if (mode === 'building' && onLocationSelect) {
        const { lng, lat } = e.lngLat
        onLocationSelect({ lat, lng })

        // Add or update marker
        if (marker.current) {
          marker.current.setLngLat([lng, lat])
        } else {
          marker.current = new mapboxgl.Marker({ color: '#2563eb' })
            .setLngLat([lng, lat])
            .addTo(map.current)
        }
      }
    })
  }, [])

  // Update marker when location changes
  useEffect(() => {
    if (selectedLocation && map.current) {
      if (marker.current) {
        marker.current.setLngLat([selectedLocation.lng, selectedLocation.lat])
      } else {
        marker.current = new mapboxgl.Marker({ color: '#2563eb' })
          .setLngLat([selectedLocation.lng, selectedLocation.lat])
          .addTo(map.current)
      }
    }
  }, [selectedLocation])

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />
      
      {mode === 'building' && !selectedLocation && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg px-6 py-3">
          <p className="text-sm font-medium text-gray-700">
            Click on the map to place a building
          </p>
        </div>
      )}
    </div>
  )
}

export default Map
