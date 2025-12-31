import React from 'react';

export const Logo = ({ className = 'h-8 w-auto', color = '#2563eb' }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 40 40"
      fill="none"
      className={className}
      aria-label="DistriHire Logo"
    >
      {/* Background Shape */}
      <rect width="40" height="40" rx="8" fill={color} fillOpacity="0.1" />

      {/* The Symbol: Interlocking paths representing distributed nodes */}
      <path
        d="M12 20C12 15.5817 15.5817 12 20 12"
        stroke={color}
        strokeWidth="3"
        strokeLinecap="round"
      />
      <path
        d="M20 28C24.4183 28 28 24.4183 28 20"
        stroke={color}
        strokeWidth="3"
        strokeLinecap="round"
      />

      {/* Nodes */}
      <circle cx="20" cy="12" r="2.5" fill={color} />
      <circle cx="28" cy="20" r="2.5" fill={color} />
      <circle cx="12" cy="20" r="2.5" fill={color} />
      <circle cx="20" cy="28" r="2.5" fill={color} />
    </svg>
  );
};
