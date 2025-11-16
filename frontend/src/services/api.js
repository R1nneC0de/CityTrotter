import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const analyzeBuilding = async (buildingData) => {
  try {
    const response = await api.post('/api/v1/analyze-building', buildingData)
    return response.data
  } catch (error) {
    console.error('Error analyzing building:', error)
    throw error
  }
}

export const getSchools = async () => {
  try {
    const response = await api.get('/api/v1/data/schools')
    return response.data
  } catch (error) {
    console.error('Error fetching schools:', error)
    throw error
  }
}

export const getZoning = async () => {
  try {
    const response = await api.get('/api/v1/data/zoning')
    return response.data
  } catch (error) {
    console.error('Error fetching zoning:', error)
    throw error
  }
}

export const getMartaStations = async () => {
  try {
    const response = await api.get('/api/v1/data/marta-stations')
    return response.data
  } catch (error) {
    console.error('Error fetching MARTA stations:', error)
    throw error
  }
}

export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

export default api

export const getImpactHeatmap = async () => {
  try {
    const response = await axios.get(`${API_URL}/analyze-building/impact-heatmap`)
    return response.data
  } catch (error) {
    console.error('Error fetching heatmap:', error)
    throw error
  }
}
