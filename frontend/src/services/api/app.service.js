import apiClient from './axiosConfig';
import { API_ROUTES } from '../../core/constants';

export const AppService = {
  submit: async (jobId, file) => {
    const formData = new FormData();
    formData.append('job_id', jobId);
    formData.append('file', file); // 'file' matches FastAPI UploadFile parameter

    const response = await apiClient.post(API_ROUTES.APPLICATIONS, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getMyApplications: async () => {
    const response = await apiClient.get(`${API_ROUTES.APPLICATIONS}/me`);
    return response.data;
  },

  getResume: async (appId) => {
    const response = await apiClient.get(
      `${API_ROUTES.APPLICATIONS}/${appId}/resume`,
      {
        responseType: 'blob', // Important for PDF streaming
      }
    );
    return response.data;
  },
};
