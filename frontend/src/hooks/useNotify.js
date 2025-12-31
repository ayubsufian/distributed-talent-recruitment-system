import { useContext, useEffect } from 'react';
import { NotificationContext } from '../context/NotificationContext';
import { useAuth } from './useAuth';

export const useNotify = (pollingInterval = 30000) => {
  const context = useContext(NotificationContext);
  const { isAuthenticated } = useAuth();

  if (!context) {
    throw new Error('useNotify must be used within a NotificationProvider');
  }

  const { fetchNotifications } = context;

  useEffect(() => {
    if (!isAuthenticated) return;

    // Initial fetch
    fetchNotifications();

    // Set up polling
    const intervalId = setInterval(() => {
      fetchNotifications();
    }, pollingInterval);

    // Cleanup on unmount
    return () => clearInterval(intervalId);
  }, [isAuthenticated, fetchNotifications, pollingInterval]);

  return context;
};
