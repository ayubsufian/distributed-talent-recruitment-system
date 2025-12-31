import React, { createContext, useState, useCallback } from 'react';
import { NotifyService } from '../services/api/notify.service';

export const NotificationContext = createContext(null);

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  const fetchNotifications = useCallback(async () => {
    try {
      const data = await NotifyService.getAll();
      setNotifications(data);
      // Calculate unread count
      const unread = data.filter((n) => !n.read_status).length;
      setUnreadCount(unread);
    } catch (error) {
      console.error('Failed to fetch notifications', error);
    }
  }, []);

  const markAsRead = async (id) => {
    try {
      // Optimistic UI update
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, read_status: true } : n))
      );
      setUnreadCount((prev) => Math.max(0, prev - 1));

      // API Call
      await NotifyService.markAsRead(id);
    } catch (error) {
      console.error('Failed to mark as read', error);
      // Revert on failure if necessary (omitted for brevity)
    }
  };

  return (
    <NotificationContext.Provider
      value={{ notifications, unreadCount, fetchNotifications, markAsRead }}
    >
      {children}
    </NotificationContext.Provider>
  );
};
