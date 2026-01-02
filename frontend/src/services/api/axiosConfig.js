import axios from 'axios';
import { TokenStorage } from '../storage/token';

/**
 * BASE_URL configuration:
 * In our Docker/Nginx setup, we leave REACT_APP_API_URL empty in the .env file.
 * This tells Axios to use relative paths, pointing to the Gateway (Port 80).
 */
const BASE_URL = process.env.REACT_APP_API_URL || '';

const apiClient = axios.create({
  baseURL: BASE_URL,
  // FIXED: Removed global 'Content-Type' header to allow automatic detection
  // for different request types (JSON vs Form-Data).
});

// Request Interceptor: Attach JWT Token from LocalStorage
apiClient.interceptors.request.use(
  (config) => {
    const token = TokenStorage.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Global Error Handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized (Expired or invalid token)
    if (error.response && error.response.status === 401) {
      TokenStorage.clearAll();

      // Avoid infinite redirects if already on login page
      if (!window.location.pathname.includes('/auth/login')) {
        window.location.href = '/auth/login';
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
