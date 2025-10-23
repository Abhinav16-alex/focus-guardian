import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Clock, Target, Flame, TrendingUp } from 'lucide-react';
import { analyticsAPI } from '../services/api';

export default function Analytics() {
  const [overview, setOverview] = useState(null);
  const [daily, setDaily] = useState([]);
  const [streaks, setStreaks] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [overviewRes, dailyRes, streaksRes] = await Promise.all([
        analyticsAPI.getOverview(7),
        analyticsAPI.getDaily(7),
        analyticsAPI.getStreaks(),
      ]);
      
      setOverview(overviewRes.data.data);
      setDaily(dailyRes.data.data);
      setStreaks(streaksRes.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm font-medium">{label}</p>
          <p className="text-3xl font-bold text-gray-800 mt-2">{value}</p>
        </div>
        <div className={`p-4 rounded-full ${color}`}>
          <Icon size={24} className="text-white" />
        </div>
      </div>
    </div>
  );

  if (!overview || !streaks) {
    return <div className="text-center py-8">Loading analytics...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={Clock}
          label="Total Focus Time"
          value={`${Math.round(overview.total_minutes)} min`}
          color="bg-blue-500"
        />
        <StatCard
          icon={Target}
          label="Sessions Completed"
          value={overview.completed_sessions}
          color="bg-green-500"
        />
        <StatCard
          icon={Flame}
          label="Current Streak"
          value={`${streaks.current} days`}
          color="bg-orange-500"
        />
        <StatCard
          icon={TrendingUp}
          label="Completion Rate"
          value={`${overview.completion_rate}%`}
          color="bg-purple-500"
        />
      </div>

      {/* Chart */}
      <div className="bg-white rounded-2xl shadow-lg p-8">
        <h3 className="text-2xl font-bold text-gray-800 mb-6">
          Last 7 Days Activity
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={daily}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { weekday: 'short' })}
            />
            <YAxis label={{ value: 'Minutes', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              formatter={(value) => [`${value} min`, 'Focus Time']}
              labelFormatter={(date) => new Date(date).toLocaleDateString()}
            />
            <Bar dataKey="minutes" fill="#3b82f6" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Streak Info */}
      <div className="bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl shadow-lg p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-semibold mb-2">🔥 Keep Your Streak Going!</h3>
            <p className="text-orange-100">
              Current: {streaks.current} days | Best: {streaks.best} days
            </p>
          </div>
          <div className="text-6xl font-bold opacity-20">
            {streaks.current}
          </div>
        </div>
      </div>
    </div>
  );
}
