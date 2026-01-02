import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { TokenStorage } from '../services/storage/token';
import { AuthService } from '../services/api/auth.service';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Helper: Converts Backend Error Objects (422s) into readable strings
  // Now includes field location for easier debugging
  const extractErrorMessage = (error, defaultMsg) => {
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;

      // Handle FastAPI array-style validation errors
      if (Array.isArray(detail)) {
        const firstError = detail[0];
        // Extract the field name (last item in loc array, e.g., ["body", "email"])
        const fieldName = firstError.loc
          ? firstError.loc[firstError.loc.length - 1]
          : 'field';
        const message = firstError.msg || 'is invalid';

        return `Error in ${fieldName}: ${message}`;
      }

      // Handle simple string errors (e.g., 401 Unauthorized)
      if (typeof detail === 'string') {
        return detail;
      }
    }

    // Fallback for network errors or other issues
    return error.response?.data?.message || error.message || defaultMsg;
  };

  // Helper: Decode JWT and set state
  const decodeAndSetUser = (token) => {
    try {
      const decoded = jwtDecode(token);
      const userData = {
        id: decoded.id,
        email: decoded.sub,
        role: decoded.role,
      };
      setUser(userData);
    } catch (error) {
      console.error('Invalid token', error);
      TokenStorage.clearAll();
      setUser(null);
    }
  };

  // Initialize: Check storage on mount
  useEffect(() => {
    const token = TokenStorage.getToken();
    if (token) {
      decodeAndSetUser(token);
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const data = await AuthService.login(email, password);
      TokenStorage.setToken(data.access_token);
      decodeAndSetUser(data.access_token);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: extractErrorMessage(error, 'Login failed'),
      };
    }
  };

  const register = async (userData) => {
    try {
      await AuthService.register(userData);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: extractErrorMessage(error, 'Registration failed'),
      };
    }
  };

  const logout = () => {
    TokenStorage.clearAll();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
