import axios from 'axios';
import { TokenStorage } from '../storage/token';

/**
 * BASE_URL configuration:
 * In our Docker/Nginx setup, we leave REACT_APP_API_URL empty in the .env file.
 * This tells Axios to use relative paths, which ensures the browser points
 * to the Nginx Gateway (Port 80) automatically.
 */
const BASE_URL = process.env.REACT_APP_API_URL || '';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach JWT Token from LocalStorage
apiClient.interceptors.request.use(
  (config) => {
    const token = TokenStorage.getToken();
    if (token) {
      // Attach the token in the format expected by FastAPI's OAuth2PasswordBearer
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
      // Clear all local session data
      TokenStorage.clearAll();

      // Force a redirect to the login page to re-authenticate
      // We use window.location.href to ensure a full page reload and clear states
      if (!window.location.pathname.includes('/auth/login')) {
        window.location.href = '/auth/login';
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
