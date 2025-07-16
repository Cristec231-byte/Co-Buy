import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AnimatedBackground from './assets/AnimatedBackground';
import './App.css';
import logo from './assets/logo.png';
import { ArrowUturnLeftIcon, KeyIcon } from '@heroicons/react/24/solid';

const AdminOTP = () => {
  const navigate = useNavigate();

  const handleVerify = (e) => {
    e.preventDefault();
    // TODO: Add OTP validation logic here
    navigate('/admin/success'); // Or your next page after OTP verification
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
            to="/admin"
            className="absolute top-4 left-4 flex h-8 w-8 items-center justify-center rounded-full
                       bg-gradient-to-br from-fuchsia-400/60 to-purple-500/40 shadow-md
                       ring-1 ring-white/40 backdrop-blur-sm hover:scale-105 transition"
          >
            <ArrowUturnLeftIcon className="h-5 w-5 text-white" />
          </Link>

          {/* Logo */}
          <img src={logo} alt="Co-Buy Logo" className="logo-img -mt-16 mb-4" />

          <h2 className="text-white text-2xl md:text-[36px] font-bold">Enter OTP</h2>
          <KeyIcon className="h-6 w-6 text-white/70 mt-4 mb-2" />

          {/* OTP Form */}
          <form onSubmit={handleVerify} className="w-full max-w-md mt-2 flex flex-col items-center space-y-6">
            {/* OTP Inputs */}
            <div className="flex justify-center gap-4">
              {[...Array(4)].map((_, index) => (
                <input
                  key={index}
                  type="text"
                  maxLength="1"
                  className="w-12 h-14 text-white text-2xl text-center bg-white/10 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-fuchsia-400 backdrop-blur-sm"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  required
                />
              ))}
            </div>

            <p className="text-white text-center text-base px-6">
              We’ve sent a 4-digit code to your email. Please enter it below to verify your identity.
            </p>

            <button type="submit" className="submit-button w-full">
              VERIFY
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AdminOTP;
