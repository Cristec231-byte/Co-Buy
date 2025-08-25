// src/MagicCallback.jsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const MagicCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Get the URL fragment (#access_token=...)
    const hash = window.location.hash;
    if (hash) {
      const params = new URLSearchParams(hash.replace("#", "?")); // replace # with ? to parse
      const accessToken = params.get("access_token");
      const refreshToken = params.get("refresh_token");

      if (accessToken) {
        // Save tokens to localStorage or context
        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken || "");

        console.log("Login successful, access token saved!");

        // Redirect user to dashboard or homepage
        navigate("/dashboard"); // adjust as needed
      } else {
        console.error("No access token found in URL fragment.");
      }
    } else {
      console.error("No URL fragment found.");
    }
  }, [navigate]);

  return (
    <div className="flex items-center justify-center h-screen">
      <p className="text-white text-lg">Logging you in...</p>
    </div>
  );
};

export default MagicCallback;
