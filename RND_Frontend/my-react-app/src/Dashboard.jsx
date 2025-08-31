// src/Dashboard.jsx
import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";
import {
  Home,
  Settings,
  LogOut,
  Search,
} from "lucide-react";
import AnimatedBackground from "./assets/AnimatedBackground";

// Sample Data
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
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="relative w-screen h-screen overflow-hidden text-white bg-background">
      {/* Background */}
      <AnimatedBackground />

      {/* Centered Dashboard Card */}
      <div className="absolute inset-0 z-10 flex items-center justify-center">
        <div className="relative flex w-full max-w-6xl rounded-3xl shadow-2xl 
                        bg-purple-950/70 backdrop-blur-2xl overflow-hidden animate-zoomIn">
          {/* Sidebar */}
          <aside className="w-64 bg-purple-900/70 backdrop-blur-xl p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center mb-10">
                <div className="w-12 h-12 rounded-full bg-white flex items-center justify-center">
                  <span className="text-black font-bold text-lg">CB</span>
                </div>
                <h2 className="ml-3 text-xl font-bold">Co-Buy</h2>
              </div>

              <nav className="space-y-4">
                <button className="flex items-center space-x-3 text-white hover:text-purple-300">
                  <Home size={20} />
                  <span>Home</span>
                </button>
                <button className="flex items-center space-x-3 text-white hover:text-purple-300">
                  <svg className="w-5 h-5" />
                  <span>Dashboard</span>
                </button>
              </nav>
            </div>

            <div className="space-y-4">
              <button className="flex items-center space-x-3 text-white hover:text-purple-300">
                <Settings size={20} />
                <span>Settings</span>
              </button>
              <button className="flex items-center space-x-3 text-white hover:text-purple-300">
                <LogOut size={20} />
                <span>Logout</span>
              </button>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1 p-8">
            {/* Header */}
            <div className="flex items-center justify-between mb-10">
              <div>
                <h1 className="text-3xl font-bold">Welcome Mr Smith!</h1>
                <p className="text-gray-300">Here is your sales forecast dashboard</p>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center bg-white bg-opacity-20 px-4 py-2 rounded-full">
                  <Search size={18} className="mr-2" />
                  <input
                    type="text"
                    placeholder="Search your query"
                    className="bg-transparent outline-none text-white placeholder-gray-300"
                  />
                </div>
                <div className="w-10 h-10 rounded-full bg-gray-600 overflow-hidden">
                  {/* Avatar placeholder */}
                </div>
              </div>
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Sales Chart */}
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-lg">
                <h2 className="text-xl font-semibold mb-4">Monthly Sales</h2>
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

              {/* Growth Chart */}
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-lg">
                <h2 className="text-xl font-semibold mb-4">Growth Over Years</h2>
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

              {/* Market Share Pie */}
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-lg lg:col-span-2">
                <h2 className="text-xl font-semibold mb-4">Market Share</h2>
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
          </main>
        </div>
      </div>
    </div>
  );
}
