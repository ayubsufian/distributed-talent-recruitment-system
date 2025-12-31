import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Sidebar = ({ links }) => {
  const location = useLocation();

  return (
    <div className="w-64 bg-gray-50 border-r border-gray-200 min-h-screen px-4 py-6">
      <ul className="space-y-2">
        {links.map((link) => (
          <li key={link.path}>
            <Link
              to={link.path}
              className={`block px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                location.pathname === link.path
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};
