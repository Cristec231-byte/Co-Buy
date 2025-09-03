// src/Dashboard.jsx
import { useEffect, useState } from "react";
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer,
  XAxis, YAxis, Tooltip, Legend
} from "recharts";
import { Home, Settings, LogOut, Search, BarChart2 } from "lucide-react";
import AnimatedBackground from "./assets/AnimatedBackground";
import "./Dashboard.css";
import { createClient } from "@supabase/supabase-js";

// ✅ Setup Supabase client
const supabaseUrl = "https://kwbgkfzvfrblsgryrlfo.supabase.co"; // your Supabase URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY; // keep in .env
const supabase = createClient(supabaseUrl, supabaseAnonKey);

const salesData = [
  { month: "Jan", sales: 400 },
  { month: "Feb", sales: 300 },
  { month: "Mar", sales: 500 },
  { month: "Apr", sales: 200 },
  { month: "May", sales: 700 },
  { month: "Jun", sales: 600 },
];

const growthData = [
  { year: "2020", value: 200 },
  { year: "2021", value: 400 },
  { year: "2022", value: 800 },
  { year: "2023", value: 1600 },
];

const pieData = [
  { name: "Product A", value: 400 },
  { name: "Product B", value: 300 },
  { name: "Product C", value: 300 },
  { name: "Product D", value: 200 },
];

const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#ff7f7f"];

export default function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [userName, setUserName] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserAndData = async () => {
      try {
        // ✅ Get current user from Supabase auth
        const {
          data: { user },
          error: userError,
        } = await supabase.auth.getUser();

        if (userError) throw userError;
        if (!user) {
          console.warn("⚠️ No user logged in.");
          setLoading(false);
          return;
        }

        console.log("✅ Supabase user:", user);

        // ✅ Fetch Name from Users table using email
        const { data: profile, error: profileError } = await supabase
          .from("Users")
          .select("Name")
          .eq("Email", user.email)
          .single();

        if (profileError) {
          console.error("❌ Error fetching profile:", profileError);
        } else {
          setUserName(profile?.Name || "");
          localStorage.setItem("sb-user-name", profile?.Name || "");
        }

        // ✅ Fetch transactions from your backend
        const accessToken = localStorage.getItem("sb-access-token");
        const res = await fetch("http://localhost:8000/transactions", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch transactions");
        const txData = await res.json();
        setTransactions(txData);
      } catch (err) {
        console.error("Error loading dashboard:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserAndData();
  }, []);

  if (loading) return <p className="text-white">Loading dashboard...</p>;

  return (
    <div className="dashboard-container">
      <AnimatedBackground />
      <div className="dashboard-wrapper">
        <div className="dashboard-card">
          {/* Sidebar */}
          <aside className="sidebar">
            <div className="sidebar-top">
              <div className="logo"><span className="logo-text">Co-Buy</span></div>
              <nav className="nav">
                <button className="nav-item"><Home size={22} /><span>Home</span></button>
                <button className="nav-item"><BarChart2 size={22} /><span>Dashboard</span></button>
              </nav>
            </div>
            <div className="sidebar-bottom">
              <button className="nav-item"><Settings size={22} /><span>Settings</span></button>
              <button className="nav-item"><LogOut size={22} /><span>Logout</span></button>
            </div>
          </aside>

          {/* Main Content */}
          <main className="main-content">
            {/* Header */}
            <div className="header">
              <div>
                <h1 className="header-title">
                  Welcome to your dashboard{userName ? `, ${userName}` : ""}!
                </h1>
                <p className="header-subtitle">Here is your personalized dashboard</p>
              </div>
              <div className="header-right">
                <div className="search-box">
                  <Search size={18} className="search-icon" />
                  <input type="text" placeholder="Search your query" className="search-input" />
                </div>
                <div className="avatar"></div>
              </div>
            </div>

            {/* Charts */}
            <div className="charts-grid">
              <div className="chart-card">
                <h2 className="chart-title">Monthly Sales</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={salesData}>
                    <XAxis dataKey="month" stroke="#fff" />
                    <YAxis stroke="#fff" />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="sales" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card">
                <h2 className="chart-title">Growth Over Years</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={growthData}>
                    <XAxis dataKey="year" stroke="#fff" />
                    <YAxis stroke="#fff" />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="value" stroke="#82ca9d" />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card wide">
                <h2 className="chart-title">Market Share</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      dataKey="value"
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      label
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Transactions */}
            <div className="chart-card wide">
              <h2 className="chart-title">Your Transactions</h2>
              {transactions.length > 0 ? (
                <table className="transactions-table">
                  <thead>
                    <tr><th>Date</th><th>Amount</th><th>Status</th></tr>
                  </thead>
                  <tbody>
                    {transactions.map((t) => (
                      <tr key={t.id}><td>{t.date}</td><td>{t.amount}</td><td>{t.status}</td></tr>
                    ))}
                  </tbody>
                </table>
              ) : (<p>No transactions available.</p>)}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
