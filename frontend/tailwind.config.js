/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');

module.exports = {
  // Scan all files in src for Tailwind classes
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      // Define a consistent primary color palette
      // We map 'primary' to blue, matching the 'bg-blue-600' used in components
      colors: {
        primary: {
          50: colors.blue[50],
          100: colors.blue[100],
          200: colors.blue[200],
          300: colors.blue[300],
          400: colors.blue[400],
          500: colors.blue[500],
          600: colors.blue[600], // Main brand color
          700: colors.blue[700],
          800: colors.blue[800],
          900: colors.blue[900],
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [
    // Provides better default styles for form elements
    // Ensure you run: npm install @tailwindcss/forms
    require('@tailwindcss/forms'),
  ],
};
