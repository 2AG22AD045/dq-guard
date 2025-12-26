import React, { useState, useEffect } from 'react';
import { Clock, Plus, Play, Pause, Trash2, Settings, Zap } from 'lucide-react';
import axios from 'axios';

const Schedule = () => {
  const [jobs, setJobs] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newJob, setNewJob] = useState({
    name: '',
    schedule: 'daily',
    data_source: {
      type: 'file',
      path: ''
    },
    alerts: {
      enabled: false,
      type: 'email',
      quality_threshold: 80,
      to_email: '',
      webhook_url: ''
    }
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      // Mock data for demo
      setJobs([
        {
          job_id: '1',
          job_name: 'Daily Sales Data Check',
          schedule_expression: 'daily',
          is_active: true,
          created_at: '2024-01-15T09:00:00Z'
        },
        {
          job_id: '2',
          job_name: 'Hourly User Activity Validation',
          schedule_expression: 'hourly',
          is_active: false,
          created_at: '2024-01-14T14:30:00Z'
        }
      ]);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    }
  };

  const createJob = async () => {
    try {
      const response = await axios.post('/schedule/validation', newJob);
      console.log('Job created:', response.data);
      
      setNewJob({
        name: '',
        schedule: 'daily',
        data_source: { type: 'file', path: '' },
        alerts: {
          enabled: false,
          type: 'email',
          quality_threshold: 80,
          to_email: '',
          webhook_url: ''
        }
      });
      setShowCreateForm(false);
      fetchJobs();
    } catch (error) {
      console.error('Error creating job:', error);
      alert('Error creating scheduled job: ' + error.message);
    }
  };

  const toggleJob = async (jobId, isActive) => {
    try {
      console.log(`Toggling job ${jobId} to ${!isActive}`);
      fetchJobs();
    } catch (error) {
      console.error('Error toggling job:', error);
    }
  };

  const deleteJob = async (jobId) => {
    if (!window.confirm('Are you sure you want to delete this scheduled job?')) {
      return;
    }
    
    try {
      console.log(`Deleting job ${jobId}`);
      fetchJobs();
    } catch (error) {
      console.error('Error deleting job:', error);
    }
  };

  const getScheduleLabel = (schedule) => {
    switch (schedule) {
      case 'daily': return 'Daily at 9:00 AM';
      case 'hourly': return 'Every hour';
      case 'weekly': return 'Weekly';
      default: return schedule;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Scheduled Validations</h1>
          <p className="text-lg text-gray-600">Automate your data quality monitoring</p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="h-5 w-5" />
          <span>Schedule New Job</span>
        </button>
      </div>

      {/* Scheduled Jobs List */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-gray-900 rounded-lg">
            <Zap className="h-5 w-5 text-white" />
          </div>
          <h2 className="text-xl font-bold text-gray-900">Active Schedules</h2>
        </div>
        
        {jobs.length === 0 ? (
          <div className="text-center py-16">
            <Clock className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-lg font-bold text-gray-900 mb-2">No scheduled jobs</h3>
            <p className="text-gray-600 mb-6">
              Create your first scheduled validation job to get started.
            </p>
            <button 
              onClick={() => setShowCreateForm(true)}
              className="btn-primary"
            >
              Create First Job
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => (
              <div key={job.job_id} className="border-2 border-gray-200 rounded-xl p-6 hover:border-gray-300 transition-all duration-200">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="p-2 bg-gray-900 rounded-lg">
                        <Settings className="h-4 w-4 text-white" />
                      </div>
                      <h3 className="text-lg font-bold text-gray-900">{job.job_name}</h3>
                    </div>
                    <p className="text-gray-600 font-medium mb-1">
                      {getScheduleLabel(job.schedule_expression)}
                    </p>
                    <p className="text-sm text-gray-500">
                      Created: {new Date(job.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <span className={`inline-flex px-3 py-1 text-sm font-bold rounded-full ${
                      job.is_active 
                        ? 'bg-green-100 text-green-800 border border-green-200' 
                        : 'bg-gray-100 text-gray-800 border border-gray-200'
                    }`}>
                      {job.is_active ? 'Active' : 'Paused'}
                    </span>
                    
                    <button
                      onClick={() => toggleJob(job.job_id, job.is_active)}
                      className={`p-3 rounded-lg transition-colors ${
                        job.is_active 
                          ? 'text-yellow-600 hover:bg-yellow-50 bg-yellow-100' 
                          : 'text-green-600 hover:bg-green-50 bg-green-100'
                      }`}
                      title={job.is_active ? 'Pause job' : 'Resume job'}
                    >
                      {job.is_active ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
                    </button>
                    
                    <button
                      onClick={() => deleteJob(job.job_id)}
                      className="p-3 text-red-600 hover:bg-red-50 bg-red-100 rounded-lg transition-colors"
                      title="Delete job"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Job Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-6 border w-11/12 md:w-3/4 lg:w-1/2 shadow-2xl rounded-2xl bg-white">
            <div className="mt-3">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-gray-900 rounded-lg">
                    <Plus className="h-5 w-5 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900">Schedule New Validation Job</h3>
                </div>
                <button
                  onClick={() => setShowCreateForm(false)}
                  className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
                >
                  ×
                </button>
              </div>
              
              <div className="space-y-6">
                {/* Job Name */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Job Name</label>
                  <input
                    type="text"
                    value={newJob.name}
                    onChange={(e) => setNewJob({...newJob, name: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                    placeholder="Enter job name"
                  />
                </div>

                {/* Schedule */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Schedule</label>
                  <select
                    value={newJob.schedule}
                    onChange={(e) => setNewJob({...newJob, schedule: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                  >
                    <option value="daily">Daily</option>
                    <option value="hourly">Hourly</option>
                    <option value="weekly">Weekly</option>
                    <option value="every_30_minutes">Every 30 minutes</option>
                  </select>
                </div>

                {/* Data Source */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">Data Source Type</label>
                  <select
                    value={newJob.data_source.type}
                    onChange={(e) => setNewJob({
                      ...newJob, 
                      data_source: {...newJob.data_source, type: e.target.value}
                    })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                  >
                    <option value="file">File</option>
                    <option value="api">API Endpoint</option>
                    <option value="database">Database Table</option>
                  </select>
                </div>

                {/* Data Source Path/URL */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    {newJob.data_source.type === 'file' ? 'File Path' : 
                     newJob.data_source.type === 'api' ? 'API URL' : 'Database Connection'}
                  </label>
                  <input
                    type="text"
                    value={newJob.data_source.path}
                    onChange={(e) => setNewJob({
                      ...newJob, 
                      data_source: {...newJob.data_source, path: e.target.value}
                    })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                    placeholder={
                      newJob.data_source.type === 'file' ? '/path/to/data.csv' :
                      newJob.data_source.type === 'api' ? 'https://api.example.com/data' :
                      'postgresql://user:pass@host:port/db'
                    }
                  />
                </div>

                {/* Alerts Section */}
                <div className="border-t pt-6">
                  <div className="flex items-center mb-4">
                    <input
                      type="checkbox"
                      checked={newJob.alerts.enabled}
                      onChange={(e) => setNewJob({
                        ...newJob,
                        alerts: {...newJob.alerts, enabled: e.target.checked}
                      })}
                      className="h-5 w-5 text-gray-900 focus:ring-gray-900 border-gray-300 rounded"
                    />
                    <label className="ml-3 text-sm font-bold text-gray-700">
                      Enable Quality Alerts
                    </label>
                  </div>

                  {newJob.alerts.enabled && (
                    <div className="space-y-4 ml-8">
                      <div>
                        <label className="block text-sm font-bold text-gray-700 mb-2">
                          Quality Threshold (%)
                        </label>
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={newJob.alerts.quality_threshold}
                          onChange={(e) => setNewJob({
                            ...newJob,
                            alerts: {...newJob.alerts, quality_threshold: parseInt(e.target.value)}
                          })}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-bold text-gray-700 mb-2">Alert Type</label>
                        <select
                          value={newJob.alerts.type}
                          onChange={(e) => setNewJob({
                            ...newJob,
                            alerts: {...newJob.alerts, type: e.target.value}
                          })}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                        >
                          <option value="email">Email</option>
                          <option value="slack">Slack</option>
                          <option value="webhook">Webhook</option>
                        </select>
                      </div>

                      {newJob.alerts.type === 'email' && (
                        <div>
                          <label className="block text-sm font-bold text-gray-700 mb-2">Email Address</label>
                          <input
                            type="email"
                            value={newJob.alerts.to_email}
                            onChange={(e) => setNewJob({
                              ...newJob,
                              alerts: {...newJob.alerts, to_email: e.target.value}
                            })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                            placeholder="admin@company.com"
                          />
                        </div>
                      )}

                      {(newJob.alerts.type === 'slack' || newJob.alerts.type === 'webhook') && (
                        <div>
                          <label className="block text-sm font-bold text-gray-700 mb-2">
                            {newJob.alerts.type === 'slack' ? 'Slack Webhook URL' : 'Webhook URL'}
                          </label>
                          <input
                            type="url"
                            value={newJob.alerts.webhook_url}
                            onChange={(e) => setNewJob({
                              ...newJob,
                              alerts: {...newJob.alerts, webhook_url: e.target.value}
                            })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                            placeholder="https://hooks.slack.com/services/..."
                          />
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
              
              <div className="mt-8 flex justify-end space-x-3">
                <button
                  onClick={() => setShowCreateForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button
                  onClick={createJob}
                  className="btn-primary"
                  disabled={!newJob.name || !newJob.data_source.path}
                >
                  Create Job
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Schedule;