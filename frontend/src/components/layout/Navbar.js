import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useNotify } from '../../hooks/useNotify';
import { ROLES } from '../../core/constants';
import { Logo } from '../../assets/images/Logo'; // <--- Import Logo

export const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { unreadCount } = useNotify();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/auth/login');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            {/* UPDATED BRANDING SECTION */}
            <Link to="/" className="flex-shrink-0 flex items-center gap-2">
              <Logo className="h-8 w-8" />
              <span className="font-bold text-xl text-gray-900">
                DistriHire
              </span>
            </Link>

            {/* Desktop Links (Unchanged) */}
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {isAuthenticated && user?.role === ROLES.CANDIDATE && (
                <>
                  <Link
                    to="/jobs"
                    className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500"
                  >
                    Jobs
                  </Link>
                  <Link
                    to="/applications/me"
                    className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500"
                  >
                    My Apps
                  </Link>
                </>
              )}
              {isAuthenticated && user?.role === ROLES.RECRUITER && (
                <Link
                  to="/recruiter/dashboard"
                  className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500"
                >
                  Dashboard
                </Link>
              )}
              {isAuthenticated && user?.role === ROLES.ADMIN && (
                <Link
                  to="/admin/dashboard"
                  className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500"
                >
                  Admin Panel
                </Link>
              )}
            </div>
          </div>

          {/* Right Side (Unchanged) */}
          <div className="flex items-center">
            {isAuthenticated ? (
              <>
                <Link
                  to="/notifications"
                  className="p-2 rounded-full text-gray-400 hover:text-gray-500 relative"
                >
                  <span className="sr-only">View notifications</span>
                  <svg
                    className="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                    />
                  </svg>
                  {unreadCount > 0 && (
                    <span className="absolute top-1 right-1 block h-2.5 w-2.5 rounded-full ring-2 ring-white bg-red-500" />
                  )}
                </Link>

                <button
                  onClick={handleLogout}
                  className="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                to="/auth/login"
                className="text-sm font-medium text-blue-600 hover:text-blue-500"
              >
                Sign in
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
