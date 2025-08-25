import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import App from './App.jsx';                // User login page
import AdminLogin from './Adminlogin.jsx';  // Admin login page
import AdminOTP from './AdminOTP.jsx';      // ✅ Add this import

import './index.css';                       // Global styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />              {/* User login */}
        <Route path="/admin" element={<AdminLogin />} />  {/* Admin login */}
        <Route path="/admin/otp" element={<AdminOTP />} /> {/* ✅ Admin OTP page */}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
