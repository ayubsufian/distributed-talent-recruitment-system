import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import { Navbar } from './components/layout/Navbar';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { ROLES } from './core/constants/index';

// Pages
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { JobSearchPage } from './pages/candidate/JobSearchPage';
import { ApplicationHistoryPage } from './pages/candidate/ApplicationHistoryPage';
import { JobManagementPage } from './pages/recruiter/JobManagementPage';
import { ApplicantReviewPage } from './pages/recruiter/ApplicantReviewPage'; // New Import
import { AdminDashboard } from './pages/admin/AdminDashboard';

// Simple Error Pages
const NotFound = () => (
  <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <h1 className="text-6xl font-bold text-gray-900">404</h1>
    <p className="mt-2 text-xl text-gray-600">Page Not Found</p>
    <a href="/" className="mt-4 text-blue-600 hover:underline">
      Go Home
    </a>
  </div>
);

const Unauthorized = () => (
  <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <h1 className="text-6xl font-bold text-red-600">403</h1>
    <p className="mt-2 text-xl text-gray-600">Unauthorized Access</p>
    <a href="/" className="mt-4 text-blue-600 hover:underline">
      Go Home
    </a>
  </div>
);

function App() {
  return (
    <AuthProvider>
      <NotificationProvider>
        <Router>
          <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar />
            <div className="flex-grow">
              <Routes>
                {/* ------------------------------------------------------- */}
                {/* Public Routes */}
                {/* ------------------------------------------------------- */}
                <Route path="/auth/login" element={<LoginPage />} />
                <Route path="/auth/register" element={<RegisterPage />} />

                {/* Default Redirect */}
                <Route path="/" element={<Navigate to="/jobs" replace />} />

                {/* ------------------------------------------------------- */}
                {/* Candidate Routes */}
                {/* ------------------------------------------------------- */}
                <Route
                  path="/jobs"
                  element={
                    <ProtectedRoute allowedRoles={[ROLES.CANDIDATE]}>
                      <JobSearchPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/applications/me"
                  element={
                    <ProtectedRoute allowedRoles={[ROLES.CANDIDATE]}>
                      <ApplicationHistoryPage />
                    </ProtectedRoute>
                  }
                />

                {/* ------------------------------------------------------- */}
                {/* Recruiter Routes */}
                {/* ------------------------------------------------------- */}
                <Route
                  path="/recruiter/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={[ROLES.RECRUITER]}>
                      <JobManagementPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/jobs/:jobId/applications"
                  element={
                    <ProtectedRoute allowedRoles={[ROLES.RECRUITER]}>
                      <ApplicantReviewPage />
                    </ProtectedRoute>
                  }
                />

                {/* ------------------------------------------------------- */}
                {/* Admin Routes */}
                {/* ------------------------------------------------------- */}
                <Route
                  path="/admin/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={[ROLES.ADMIN]}>
                      <AdminDashboard />
                    </ProtectedRoute>
                  }
                />

                {/* ------------------------------------------------------- */}
                {/* Error Routes */}
                {/* ------------------------------------------------------- */}
                <Route path="/unauthorized" element={<Unauthorized />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </div>
          </div>
        </Router>
      </NotificationProvider>
    </AuthProvider>
  );
}

export default App;
