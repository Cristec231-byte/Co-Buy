import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AnimatedBackground from './assets/AnimatedBackground';
import './App.css';
import logo from './assets/logo.png';
import { EnvelopeIcon, ArrowUturnLeftIcon, UserIcon } from '@heroicons/react/24/solid';

const AdminLogin = () => {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Add actual email validation / API call here if needed
    // After sending OTP...
    navigate('/admin/otp'); // Change this path to match your OTP page route
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden">
      <AnimatedBackground />

      {/* Top Heading */}
      <div className="absolute top-8 w-full z-10 text-center">
        <h1 className="main-title">Co-Buy Property</h1>
        <p className="subtitle">REALESTATE</p>
      </div>

      {/* Glass Card */}
      <div className="absolute inset-0 z-10 flex items-center justify-center pt-20">
        <div className="login-box relative flex flex-col items-center">
          {/* Back arrow */}
          <Link
            to="/"
            className="absolute top-4 left-4 flex h-8 w-8 items-center justify-center rounded-full
                       bg-gradient-to-br from-fuchsia-400/60 to-purple-500/40 shadow-md
                       ring-1 ring-white/40 backdrop-blur-sm hover:scale-105 transition"
          >
            <ArrowUturnLeftIcon className="h-5 w-5 text-white" />
          </Link>

          {/* Logo */}
          <img src={logo} alt="Co-Buy Logo" className="logo-img -mt-16 mb-4" />

          <h2 className="text-white text-2xl md:text-[36px] font-bold">Admin Portal</h2>
          <UserIcon className="h-6 w-6 text-white/70 mt-4 mb-2" />

          {/* Email Input */}
          <form onSubmit={handleSubmit} className="w-full max-w-md mt-2 flex flex-col items-center space-y-4">
            <div className="relative w-full">
              <EnvelopeIcon className="h-5 w-5 text-white absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                type="email"
                placeholder="ENTER EMAIL"
                className="input-field w-full pl-10"
                required
              />
            </div>

            <p className="text-white md:text-[18px] text-center pb-6">
              Please enter the email associated with your account.
            </p>

            <button type="submit" className="submit-button w-full">
              SEND OTP
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
