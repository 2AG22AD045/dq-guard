import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, Database, FileCheck, AlertCircle, RefreshCw, Upload, History, Clock, Zap, Shield, BarChart } from 'lucide-react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [summaryRes, trendsRes] = await Promise.all([
        axios.get('/dashboard/summary'),
        axios.get('/dashboard/trends')
      ]);
      
      setSummary(summaryRes.data);
      setTrends(trendsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const pieColors = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444'];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Data Quality Dashboard</h1>
          <p className="text-lg text-gray-600">Monitor and maintain your data quality standards</p>
        </div>
        <div className="flex space-x-3">
          <button 
            onClick={fetchDashboardData}
            className="btn-dark flex items-center space-x-2"
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/validate" className="feature-card group">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-gray-900 rounded-xl text-white group-hover:bg-gray-800 transition-colors">
              <Upload className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900">Validate Data</h3>
              <p className="text-gray-600">Upload and check data quality</p>
            </div>
          </div>
        </Link>

        <Link to="/history" className="feature-card group">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-gray-900 rounded-xl text-white group-hover:bg-gray-800 transition-colors">
              <History className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900">View History</h3>
              <p className="text-gray-600">Browse validation reports</p>
            </div>
          </div>
        </Link>

        <Link to="/schedule" className="feature-card group">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-gray-900 rounded-xl text-white group-hover:bg-gray-800 transition-colors">
              <Clock className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900">Schedule Jobs</h3>
              <p className="text-gray-600">Automate quality checks</p>
            </div>
          </div>
        </Link>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Total Validations</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{summary?.total_validations || 0}</p>
            </div>
            <div className="p-3 bg-gray-900 rounded-xl">
              <FileCheck className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Avg Quality Score</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{summary?.average_quality_score || 0}%</p>
            </div>
            <div className="p-3 bg-gray-900 rounded-xl">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Data Sources</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{summary?.unique_sources || 0}</p>
            </div>
            <div className="p-3 bg-gray-900 rounded-xl">
              <Database className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Issues Found</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {summary?.quality_distribution?.Poor || 0}
              </p>
            </div>
            <div className="p-3 bg-gray-900 rounded-xl">
              <AlertCircle className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Quality Trends Chart */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gray-900 rounded-lg">
                <BarChart className="h-5 w-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-gray-900">Quality Trends</h2>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trends?.daily_trends || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="date" stroke="#64748b" />
              <YAxis domain={[0, 100]} stroke="#64748b" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: 'white'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="average_score" 
                stroke="#1f2937" 
                strokeWidth={3}
                dot={{ fill: '#1f2937', strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8, fill: '#1f2937' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Quality Distribution */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gray-900 rounded-lg">
                <Shield className="h-5 w-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-gray-900">Quality Distribution</h2>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={Object.entries(summary?.quality_distribution || {}).map(([key, value]) => ({
                  name: key,
                  value: value
                }))}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {Object.entries(summary?.quality_distribution || {}).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1f2937', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: 'white'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Validations */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gray-900 rounded-lg">
              <Zap className="h-5 w-5 text-white" />
            </div>
            <h2 className="text-xl font-bold text-gray-900">Recent Validations</h2>
          </div>
          <Link to="/history" className="btn-outline-dark">
            View All
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Source
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Quality Score
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {summary?.recent_validations?.map((validation, index) => (
                <tr key={index} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                    {validation.source}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className={`inline-flex px-3 py-1 text-xs font-bold rounded-full ${
                      validation.quality_score >= 90 ? 'bg-green-100 text-green-800' :
                      validation.quality_score >= 70 ? 'bg-blue-100 text-blue-800' :
                      validation.quality_score >= 50 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {validation.quality_score}%
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {new Date(validation.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-3 py-1 text-xs font-bold rounded-full ${
                      validation.quality_score >= 70 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {validation.quality_score >= 70 ? 'Passed' : 'Failed'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;