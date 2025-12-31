import apiClient from './axiosConfig';
import { API_ROUTES } from '../../core/constants';

export const JobService = {
  getAll: async (params = {}) => {
    // params can be { q: 'search term', limit: 10, offset: 0 }
    const response = await apiClient.get(API_ROUTES.JOBS, { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await apiClient.get(`${API_ROUTES.JOBS}/${id}`);
    return response.data;
  },

  create: async (jobData) => {
    const response = await apiClient.post(API_ROUTES.JOBS, jobData);
    return response.data;
  },

  delete: async (id) => {
    const response = await apiClient.delete(`${API_ROUTES.JOBS}/${id}`);
    return response.data;
  },
};
