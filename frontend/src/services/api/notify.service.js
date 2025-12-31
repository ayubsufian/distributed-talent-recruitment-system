import apiClient from './axiosConfig';
import { API_ROUTES } from '../../core/constants';

export const NotifyService = {
  getAll: async () => {
    const response = await apiClient.get(API_ROUTES.NOTIFICATIONS);
    return response.data;
  },

  markAsRead: async (id) => {
    const response = await apiClient.patch(
      `${API_ROUTES.NOTIFICATIONS}/${id}/read`
    );
    return response.data;
  },
};
