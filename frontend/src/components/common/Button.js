import React from 'react';
import { Spinner } from './Spinner';

const variants = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
  outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50',
};

export const Button = ({
  children,
  variant = 'primary',
  isLoading = false,
  className = '',
  ...props
}) => {
  return (
    <button
      className={`px-4 py-2 rounded-md font-medium transition duration-200 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed ${variants[variant]} ${className}`}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading && <Spinner size="sm" className="mr-2 text-current" />}
      {children}
    </button>
  );
};
