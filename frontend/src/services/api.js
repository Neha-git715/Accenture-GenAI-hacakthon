import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
});

// Enhanced request logger
const requestLogger = (config) => {
  if (process.env.NODE_ENV === 'development') {
    console.debug('API Request:', {
      method: config.method.toUpperCase(),
      url: config.url,
      params: config.params,
      data: config.data
    });
  }
  return config;
};

// Enhanced error handler
const errorHandler = (error) => {
  if (process.env.NODE_ENV === 'development') {
    const errorData = {
      message: error.message,
      config: {
        url: error.config?.url,
        method: error.config?.method
      }
    };

    if (error.response) {
      errorData.status = error.response.status;
      errorData.data = error.response.data;
    } else if (error.request) {
      errorData.request = error.request;
    }

    console.error('API Error:', errorData);
  }

  // Transform error response for consistent handling
  if (error.response) {
    const apiError = new Error(error.response.data?.detail || 'API request failed');
    apiError.status = error.response.status;
    apiError.data = error.response.data;
    return Promise.reject(apiError);
  }
  return Promise.reject(error);
};

api.interceptors.request.use(requestLogger);
api.interceptors.response.use(response => response, errorHandler);

// Auth token management
const getAuthToken = () => localStorage.getItem('authToken');

api.interceptors.request.use(config => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API service with all endpoints matching FastAPI backend
export const bankGenApi = {
  // Data Products CRUD
  getDataProducts: () => api.get('/data-products'),
  getDataProduct: (id) => api.get(`/data-products/${id}`),
  createDataProduct: (data) => api.post('/data-products', data),
  updateDataProduct: (id, data) => api.patch(`/data-products/${id}`, data),
  deleteDataProduct: (id) => api.delete(`/data-products/${id}`),

  // GenAI Endpoints
  generateDataProductStructure: (productId) => 
    api.post(`/data-products/${productId}/generate-structure`),
  generateSourceMappings: (productId) => 
    api.post(`/data-products/${productId}/generate-mappings`),
  validateDataProduct: (productId) => 
    api.get(`/data-products/${productId}/validate`),

  // Source System Management
  getSourceSystems: () => api.get('/source-systems'),
  getSourceSystemAttributes: (systemId) => 
    api.get(`/source-systems/${systemId}/attributes`),

  // Utility Endpoints
  checkHealth: () => api.get('/health'),
  getApiVersion: () => api.get('/version')
};

// Add types for TypeScript (remove if not using TS)
/*
 * @typedef {Object} DataProduct
 * @property {number} id
 * @property {string} name
 * @property {string} description
 * @property {'Draft'|'Active'|'Archived'} status
 * @property {string} refresh_frequency
 * @property {string} last_updated
 * @property {Object|null} structure
 * @property {Object|null} source_mappings
 */

export default api;