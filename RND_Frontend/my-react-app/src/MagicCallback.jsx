// src/MagicCallback.jsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

const MagicCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleMagicLink = async () => {
      const hash = window.location.hash;
      if (!hash) return;

      const params = new URLSearchParams(hash.replace("#", "?"));
      const accessToken = params.get("access_token");
      const refreshToken = params.get("refresh_token");

      if (!accessToken) return;

      try {
        await supabase.auth.setSession({
          access_token: accessToken,
          refresh_token: refreshToken || "",
        });

        localStorage.setItem("sb-access-token", accessToken);
        localStorage.setItem("sb-refresh-token", refreshToken || "");

        // ✅ Get user info (name should be here)
        const { data: userData, error } = await supabase.auth.getUser();
        if (error) {
          console.error("Error fetching user:", error);
        } else {
          const user = userData.user;

          // Try different metadata keys for name
          const name =
            user?.user_metadata?.full_name ||
            user?.user_metadata?.name ||
            user?.user_metadata?.display_name ||
            user?.email;

          localStorage.setItem("sb-user-name", name);
          console.log("✅ Saved user name:", name);
        }

        navigate("/dashboard");
      } catch (err) {
        console.error("Error handling magic link:", err);
      }
    };

    handleMagicLink();
  }, [navigate]);

  return (
    <div className="flex items-center justify-center h-screen">
      <p className="text-black text-lg">Logging you in...</p>
    </div>
  );
};

export default MagicCallback;
