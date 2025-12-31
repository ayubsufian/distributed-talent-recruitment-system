import React from 'react';

const timeAgo = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  if (seconds < 60) return 'Just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
};

export const NotificationItem = ({ notification, onRead }) => {
  return (
    <div
      className={`p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer ${
        !notification.read_status ? 'bg-blue-50' : 'bg-white'
      }`}
      onClick={() => onRead(notification.id)}
    >
      <div className="flex justify-between items-start">
        <p
          className={`text-sm ${
            !notification.read_status
              ? 'font-semibold text-gray-900'
              : 'text-gray-600'
          }`}
        >
          {notification.message}
        </p>
        {!notification.read_status && (
          <span className="h-2 w-2 bg-blue-600 rounded-full flex-shrink-0 mt-1.5 ml-2"></span>
        )}
      </div>
      <p className="text-xs text-gray-400 mt-1">
        {timeAgo(notification.created_at)}
      </p>
    </div>
  );
};
