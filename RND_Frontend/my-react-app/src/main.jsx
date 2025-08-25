import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import App from './App.jsx';                // User login page
import MagicCallback from './MagicCallback.jsx'; // User magic link callback
import Dashboard from './Dashboard.jsx';        // User dashboard

import './index.css';                       // Global styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        {/* User login */}
        <Route path="/" element={<App />} />

        {/* Magic link callback */}
        <Route path="/magic-callback" element={<MagicCallback />} />

        {/* User dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
