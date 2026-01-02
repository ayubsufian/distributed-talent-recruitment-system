import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Card } from '../../components/common/Card';
import { FormField } from '../../components/forms/FormField';
import { ROLES } from '../../core/constants';
import { Logo } from '../../assets/images/Logo';

export const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    role: ROLES.CANDIDATE, // Default value
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  // Updates the state based on input 'name' attribute
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    // --- DEBUG: Check your console (F12) to see if all 3 fields are here ---
    console.log('Submitting to Backend:', formData);

    const result = await register(formData);

    if (result.success) {
      // Success: Proceed to login
      navigate('/auth/login');
    } else {
      // result.error is now a descriptive string from AuthContext
      setError(result.error);
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center mb-4">
          <Logo className="h-12 w-12" />
        </div>
        <h2 className="text-center text-3xl font-extrabold text-gray-900">
          Join DistriHire
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card>
          {/* --- Detailed Error Alert --- */}
          {error && (
            <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4 animate-fade-in">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-red-400"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-700 font-medium">{error}</p>
                </div>
              </div>
            </div>
          )}

          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Email Input */}
            <FormField label="Email address">
              <Input
                name="email"
                type="email"
                placeholder="you@example.com"
                required
                autoComplete="email"
                value={formData.email}
                onChange={handleChange}
              />
            </FormField>

            {/* Password Input */}
            <FormField label="Password">
              <Input
                name="password"
                type="password"
                placeholder="••••••••"
                required
                autoComplete="new-password"
                value={formData.password}
                onChange={handleChange}
              />
            </FormField>

            {/* Role Selection Dropdown */}
            <FormField label="I am a...">
              <select
                name="role"
                value={formData.role}
                onChange={handleChange}
                className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md appearance-none bg-white"
                required
              >
                <option value={ROLES.CANDIDATE}>Candidate</option>
                <option value={ROLES.RECRUITER}>Recruiter</option>
              </select>
            </FormField>

            <Button
              type="submit"
              className="w-full py-3"
              isLoading={isSubmitting}
            >
              Create Account
            </Button>
          </form>

          <div className="mt-6 text-center">
            <Link
              to="/auth/login"
              className="font-medium text-blue-600 hover:text-blue-500 text-sm"
            >
              Already have an account? Sign in
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
};
