import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.YOUR_MAPBOX_TOKEN_HERE'

function Map({ selectedLocation, buildingFootprint, analysisResults, onLocationSelect, mode, buildingStories }) {
  const mapContainer = useRef(null)
  const map = useRef(null)
  const marker = useRef(null)

  useEffect(() => {
    if (map.current) return

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-84.3880, 33.7490],
      zoom: 15,
      pitch: 45,
      bearing: -17.6
    })

    map.current.on('load', () => {
      const layers = map.current.getStyle().layers
      const labelLayerId = layers.find(
        (layer) => layer.type === 'symbol' && layer.layout['text-field']
      ).id

      map.current.addLayer(
        {
          'id': '3d-buildings',
          'source': 'composite',
          'source-layer': 'building',
          'filter': ['==', 'extrude', 'true'],
          'type': 'fill-extrusion',
          'minzoom': 15,
          'paint': {
            'fill-extrusion-color': '#aaa',
            'fill-extrusion-height': [
              'interpolate',
              ['linear'],
              ['zoom'],
              15,
              0,
              15.05,
              ['get', 'height']
            ],
            'fill-extrusion-base': [
              'interpolate',
              ['linear'],
              ['zoom'],
              15,
              0,
              15.05,
              ['get', 'min_height']
            ],
            'fill-extrusion-opacity': 0.6
          }
        },
        labelLayerId
      )
    })

    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right')
  }, [])

  // Handle map clicks
  useEffect(() => {
    if (!map.current) return

    const handleClick = (e) => {
      if (mode === 'building' && onLocationSelect) {
        const { lng, lat } = e.lngLat
        onLocationSelect({ lat, lng })

        if (marker.current) {
          marker.current.setLngLat([lng, lat])
        } else {
          marker.current = new mapboxgl.Marker({ color: '#2563eb' })
            .setLngLat([lng, lat])
            .addTo(map.current)
        }

        addBuildingPreview(lng, lat, buildingStories * 12)
      }
    }

    map.current.on('click', handleClick)

    return () => {
      if (map.current) {
        map.current.off('click', handleClick)
      }
    }
  }, [mode, onLocationSelect, buildingStories])

  // Update building when stories change
  useEffect(() => {
    if (selectedLocation && buildingStories && map.current) {
      addBuildingPreview(selectedLocation.lng, selectedLocation.lat, buildingStories * 12)
    }
  }, [buildingStories, selectedLocation])

  const addBuildingPreview = (lng, lat, height) => {
    if (!map.current) return

    if (map.current.getLayer('building-preview')) {
      map.current.removeLayer('building-preview')
      map.current.removeSource('building-preview')
    }

    const size = 0.0005
    const coordinates = [
      [
        [lng - size, lat - size],
        [lng + size, lat - size],
        [lng + size, lat + size],
        [lng - size, lat + size],
        [lng - size, lat - size]
      ]
    ]

    map.current.addSource('building-preview', {
      'type': 'geojson',
      'data': {
        'type': 'Feature',
        'geometry': {
          'type': 'Polygon',
          'coordinates': coordinates
        }
      }
    })

    map.current.addLayer({
      'id': 'building-preview',
      'type': 'fill-extrusion',
      'source': 'building-preview',
      'paint': {
        'fill-extrusion-color': '#3b82f6',
        'fill-extrusion-height': height,
        'fill-extrusion-base': 0,
        'fill-extrusion-opacity': 0.5
      }
    })

    map.current.flyTo({
      center: [lng, lat],
      zoom: 17,
      pitch: 60,
      bearing: -20,
      duration: 1500
    })
  }

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />
      
      {mode === 'building' && !selectedLocation && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg px-6 py-3 pointer-events-none z-10">
          <p className="text-sm font-medium text-gray-700">
            👆 Click on the map to place a building
          </p>
        </div>
      )}

      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg px-4 py-2 text-xs text-gray-600 pointer-events-none">
        <p>🖱️ Right-click + drag to rotate</p>
        <p>🎚️ Ctrl + drag to change pitch</p>
      </div>
    </div>
  )
}

export default Map