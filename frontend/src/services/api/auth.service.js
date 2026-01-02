import apiClient from './axiosConfig';
import { API_ROUTES } from '../../core/constants';

export const AuthService = {
  login: async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    // Verify there is only ONE slash between the variable and 'login'
    const response = await apiClient.post(`${API_ROUTES.AUTH}/login`, formData);
    return response.data;
  },

  register: async (userData) => {
    // Verify there is only ONE slash here too
    const response = await apiClient.post(
      `${API_ROUTES.AUTH}/register`,
      userData
    );
    return response.data;
  },

  getMe: async () => {
    const response = await apiClient.get(`${API_ROUTES.USERS}/me`);
    return response.data;
  },
};
