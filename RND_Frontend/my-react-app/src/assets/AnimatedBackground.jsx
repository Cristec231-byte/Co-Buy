import React from 'react';

const AnimatedBackground = () => {
  return (
    <div className="relative w-screen h-screen bg-[#291740] overflow-hidden">
      {/* Blob 1 */}
      <div
        className="absolute top-[10%] left-[10%] w-[400px] h-[400px] bg-[#3f5784] rounded-full filter blur-3xl opacity-70 animate-blob"
      ></div>

      {/* Blob 2 */}
      <div
        className="absolute top-[50%] left-[20%] w-[500px] h-[500px] bg-[#345d5b] rounded-full filter blur-3xl opacity-70 animate-blob"
      ></div>

      {/* Blob 3 */}
      <div
        className="absolute bottom-[15%] right-[15%] w-[450px] h-[450px] bg-[#54577e] rounded-full filter blur-3xl opacity-70 animate-blob"
      ></div>
    </div>
  );
};

export default AnimatedBackground;