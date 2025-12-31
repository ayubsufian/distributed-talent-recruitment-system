import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { TokenStorage } from '../services/storage/token';
import { AuthService } from '../services/api/auth.service';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Helper: Converts Backend Error Objects (422s) into readable strings
  const extractErrorMessage = (error, defaultMsg) => {
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;

      // FastAPI/Pydantic returns validation errors as an array of objects
      if (Array.isArray(detail)) {
        // Return the first error message (e.g., "value is not a valid email")
        return detail[0].msg || defaultMsg;
      }

      // If it's just a plain string (like a 401 or 400 error)
      if (typeof detail === 'string') {
        return detail;
      }
    }
    return error.message || defaultMsg;
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
