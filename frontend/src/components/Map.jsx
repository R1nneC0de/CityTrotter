import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css'

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || 'pk.YOUR_MAPBOX_TOKEN_HERE'

function Map({ selectedLocation, buildingFootprint, analysisResults, onLocationSelect, mode, buildingStories, buildingArea, onLocationChange }) {
  const mapContainer = useRef(null)
  const map = useRef(null)
  const marker = useRef(null)
  const dragEndTimer = useRef(null)

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
      )?.id

      if (labelLayerId) {
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
      }
    })

    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right')
  }, [])

  // Add geocoder (search box)
  useEffect(() => {
    if (!map.current) return

    const geocoder = new MapboxGeocoder({
      accessToken: mapboxgl.accessToken,
      mapboxgl: mapboxgl,
      marker: false,
      placeholder: 'Search Atlanta address...',
      bbox: [-84.55, 33.65, -84.29, 33.89],
      proximity: { longitude: -84.3880, latitude: 33.7490 },
      countries: 'us'
    })

    map.current.addControl(geocoder, 'top-left')

    geocoder.on('result', (e) => {
      const coords = e.result.center
      if (mode === 'building' && onLocationSelect) {
        onLocationSelect({ lng: coords[0], lat: coords[1] })
        if (!marker.current) {
          createDraggableMarker(coords[0], coords[1])
          addBuildingPreview(coords[0], coords[1], buildingStories * 12, buildingArea)
        }
      }
    })

    return () => {
      map.current.removeControl(geocoder)
    }
  }, [mode, onLocationSelect, buildingStories, buildingArea])

  // Handle map clicks
  useEffect(() => {
    if (!map.current) return

    let isDragging = false

    const handleClick = (e) => {
      if (isDragging) {
        isDragging = false
        return
      }

      if (mode === 'building' && onLocationSelect && !marker.current) {
        const { lng, lat } = e.lngLat
        onLocationSelect({ lat, lng })
        createDraggableMarker(lng, lat)
        addBuildingPreview(lng, lat, buildingStories * 12, buildingArea)
      }
    }

    const handleMouseDown = () => {
      if (marker.current) {
        isDragging = true
      }
    }

    map.current.on('click', handleClick)
    map.current.on('mousedown', handleMouseDown)

    return () => {
      if (map.current) {
        map.current.off('click', handleClick)
        map.current.off('mousedown', handleMouseDown)
      }
    }
  }, [mode, onLocationSelect, buildingStories, buildingArea])

  const createDraggableMarker = (lng, lat) => {
    marker.current = new mapboxgl.Marker({ 
      color: '#2563eb',
      draggable: true
    })
      .setLngLat([lng, lat])
      .addTo(map.current)

    let wasDragged = false

    marker.current.on('dragstart', () => {
      wasDragged = true
    })

    marker.current.on('drag', () => {
      const lngLat = marker.current.getLngLat()
      addBuildingPreview(lngLat.lng, lngLat.lat, buildingStories * 12, buildingArea, false)
    })

    marker.current.on('dragend', () => {
      const lngLat = marker.current.getLngLat()
      
      if (dragEndTimer.current) {
        clearTimeout(dragEndTimer.current)
      }

      dragEndTimer.current = setTimeout(() => {
        if (onLocationChange && wasDragged) {
          onLocationChange({ lat: lngLat.lat, lng: lngLat.lng })
        }
        wasDragged = false
      }, 1000)
    })
  }

  const removeBuildingPreview = () => {
    if (!map.current) return
    
    if (map.current.getLayer('building-preview')) {
      map.current.removeLayer('building-preview')
    }
    
    if (map.current.getSource('building-preview')) {
      map.current.removeSource('building-preview')
    }
    
    if (marker.current) {
      marker.current.remove()
      marker.current = null
    }
  }

  useEffect(() => {
    if (selectedLocation && map.current) {
      addBuildingPreview(
        selectedLocation.lng, 
        selectedLocation.lat, 
        buildingStories * 12,
        buildingArea,
        false
      )
    }
  }, [buildingStories, buildingArea, selectedLocation])

  useEffect(() => {
    if (!selectedLocation) {
      removeBuildingPreview()
    }
  }, [selectedLocation])

  const addBuildingPreview = (lng, lat, height, area = 2500, animate = true) => {
    if (!map.current) return

    if (map.current.getLayer('building-preview')) {
      map.current.removeLayer('building-preview')
      map.current.removeSource('building-preview')
    }

    const sideLengthFeet = Math.sqrt(area)
    const sideLengthDegrees = sideLengthFeet / 305000
    const halfSize = sideLengthDegrees / 2
    const coordinates = [
      [
        [lng - halfSize, lat - halfSize],
        [lng + halfSize, lat - halfSize],
        [lng + halfSize, lat + halfSize],
        [lng - halfSize, lat + halfSize],
        [lng - halfSize, lat - halfSize]
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

    if (animate) {
      map.current.flyTo({
        center: [lng, lat],
        zoom: 17,
        pitch: 60,
        bearing: -20,
        duration: 1500
      })
    }
  }

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />
      
      {mode === 'building' && !selectedLocation && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg px-6 py-3 pointer-events-none z-10">
          <p className="text-sm font-medium text-gray-700">
            👆 Click on map or search for an address
          </p>
        </div>
      )}

      {mode === 'building' && selectedLocation && !analysisResults && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 bg-blue-50 border border-blue-200 rounded-lg shadow-lg px-6 py-3 pointer-events-none z-10">
          <p className="text-sm font-medium text-blue-800">
            🖱️ Drag the marker to move the building
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