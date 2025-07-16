import React from 'react';
import { Link } from 'react-router-dom'; // ✅ required for <Link>
import AnimatedBackground from './assets/AnimatedBackground';
import './App.css';
import logo from './assets/logo.png';
import { EnvelopeIcon } from '@heroicons/react/24/solid';

const App = () => {
  return (
    <div className="relative w-screen h-screen overflow-hidden">
      <AnimatedBackground />

      {/* Top Heading Section */}
      <div className="absolute top-8 w-full z-10 text-center">
        <h1 className="main-title">Co-Buy Property</h1>
        <p className="subtitle">REALESTATE</p>
      </div>

      {/* Centered Login Section */}
      <div className="absolute inset-0 z-10 flex items-center justify-center pt-20">
        <div className="login-box flex flex-col items-center">
          {/* Logo */}
          <img src={logo} alt="Co-Buy Logo" className="logo-img -mt-20 mb-4" />

          {/* Greeting */}
          <h2 className="text-white text-2xl md:text-[36px] font-bold pt-10">Hi, Welcome! 👋</h2>

          {/* Email Input */}
          <form className="w-full max-w-md mt-4 flex flex-col items-center space-y-4 pt-15">
            <div className="relative w-full">
              <EnvelopeIcon className="h-5 w-5 text-white absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none" />
              <input
                type="email"
                placeholder="Enter Email"
                className="input-field w-full pl-10"
              />
            </div>
            <p className="text-white md:text-[18px] text-center pt-4 pb-10">
              Please enter the email associated with your account.
            </p>
            <button type="submit" className="submit-button w-full">
              SEND OTP
            </button>
          </form>

          
          {/* 👤 Admin Link */}
          <Link
            to="/admin"
            className="text-white/70 mt-6 md:text-[20px] pt-20 hover:text-white transition-colors"
          >
            👤 Admin
          </Link>
         
        </div>
      </div>
    </div>
  );
};

export default App;