import React from 'react';

const AnimatedBackground = () => {
  return (
    <div className="relative w-screen h-screen overflow-hidden">
      <div className="absolute w-full h-full bg-gradient-to-r from-purple-500 via-blue-500 to-green-500 bg-[length:200%_200%] animate-gradient"></div>
      <div className="absolute inset-0">
        {/* Add optional additional layer */}
      </div>
    </div>
  );
};

export default AnimatedBackground;