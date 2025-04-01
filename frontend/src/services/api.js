import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for API calls
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', {
      url: config.url,
      method: config.method,
      data: config.data,
      headers: config.headers
    });
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for API calls
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      status: response.status,
      data: response.data,
      headers: response.headers
    });
    return response;
  },
  async (error) => {
    console.error('API Error:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      config: error.config
    });

    if (error.response) {
      // Handle specific error cases here
      switch (error.response.status) {
        case 401:
          console.error('Unauthorized access');
          break;
        case 403:
          console.error('Forbidden access');
          break;
        case 404:
          console.error('Resource not found');
          break;
        case 500:
          console.error('Server error');
          break;
        default:
          console.error('API error occurred');
      }
    } else if (error.request) {
      console.error('No response received from server');
    } else {
      console.error('Error setting up request:', error.message);
    }

    return Promise.reject(error);
  }
);

// API endpoints matching FastAPI backend
export const bankGenApi = {
  // Data Products
  getDataProducts: () => axios.get(`${API_BASE_URL}/api/data-products`),
  createDataProduct: (data) => axios.post(`${API_BASE_URL}/api/data-products`, data),
  updateDataProduct: (id, data) => axios.put(`${API_BASE_URL}/api/data-products/${id}`, data),
  deleteDataProduct: (id) => axios.delete(`${API_BASE_URL}/api/data-products/${id}`),
  
  // Recommendations
  recommendAttributes: (data) => axios.post(`${API_BASE_URL}/api/recommend-attributes`, data),
  
  // Design and Validation
  designDataProduct: (data) => axios.post(`${API_BASE_URL}/api/design-product`, data),
  validateDataProduct: (data) => axios.post(`${API_BASE_URL}/api/validate-product`, data),
};

export default api; 