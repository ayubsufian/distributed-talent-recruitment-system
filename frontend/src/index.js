import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Create the root element
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App within StrictMode for development checks
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
