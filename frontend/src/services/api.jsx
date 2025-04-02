import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints matching FastAPI backend
export const bankGenApi = {
  // Data Products
  getDataProducts: () => api.get('/data-products'),
  getDataProduct: (id) => api.get(`/data-products/${id}`),
  createDataProduct: (data) => api.post('/data-products', data),
  updateDataProduct: (id, data) => api.put(`/data-products/${id}`, data),
  deleteDataProduct: (id) => api.delete(`/data-products/${id}`),
  
  // Data Product Design
  analyzeRequirements: (data) => api.post('/analyze-requirements', data),
  designDataProduct: (data) => api.post('/design-data-product', data),
  mapAttributes: (data) => api.post('/map-attributes', data),
  validateDataProduct: (id) => api.post(`/validate-data-product/${id}`),
  
  // Authentication
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
  refreshToken: () => api.post('/auth/refresh-token'),
  
  // User Management
  getCurrentUser: () => api.get('/users/me'),
  updateUserProfile: (data) => api.put('/users/me', data),
  changePassword: (data) => api.put('/users/me/password', data),
};

export default bankGenApi;