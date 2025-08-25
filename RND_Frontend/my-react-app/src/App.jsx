import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import AnimatedBackground from './assets/AnimatedBackground';
import './App.css';
import logo from './assets/logo.png';
import { EnvelopeIcon } from '@heroicons/react/24/solid';

const App = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/request-magic-link', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Email: email }), // must match FastAPI model
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`Magic link sent! Check your email or click here: ${data.link}`);
      } else {
        setMessage(`Error: ${data.detail}`);
      }
    } catch (err) {
      setMessage(`Request failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

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
          <img src={logo} alt="Co-Buy Logo" className="logo-img -mt-20 mb-4" />

          <h2 className="text-white text-2xl md:text-[36px] font-bold pt-10">Hi, Welcome! 👋</h2>

          {/* Email Input */}
          <form
            className="w-full max-w-md mt-4 flex flex-col items-center space-y-4 pt-15"
            onSubmit={handleSubmit}
          >
            <div className="relative w-full">
              <EnvelopeIcon className="h-5 w-5 text-white absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none" />
              <input
                type="email"
                placeholder="Enter Email"
                className="input-field w-full pl-10"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <p className="text-white md:text-[18px] text-center pt-4 pb-10">
              Please enter the email associated with your account.
            </p>
            <button
              type="submit"
              className="submit-button w-full"
              disabled={loading}
            >
              {loading ? 'Sending...' : 'SEND OTP'}
            </button>
          </form>

          {message && (
            <p className="text-white mt-4 text-center md:text-[16px] break-words">
              {message}
            </p>
          )}

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
