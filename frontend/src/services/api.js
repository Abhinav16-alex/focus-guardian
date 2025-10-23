import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Focus Session API
export const focusAPI = {
  start: (duration, mode) => 
    api.post('/focus/start', { duration, mode }),
  stop: (completed) => 
    api.post('/focus/stop', { completed }),
  getStatus: () => 
    api.get('/focus/status'),
};

// Blocklist API
export const blocklistAPI = {
  getAll: () => 
    api.get('/blocklist'),
  add: (url, category) => 
    api.post('/blocklist', { url, category }),
  remove: (siteId) => 
    api.delete(`/blocklist/${siteId}`),
  addPreset: (category) => 
    api.post(`/blocklist/preset/${category}`),
};

// Analytics API
export const analyticsAPI = {
  getOverview: (days = 7) => 
    api.get(`/analytics/overview?days=${days}`),
  getDaily: (days = 30) => 
    api.get(`/analytics/daily?days=${days}`),
  getStreaks: () => 
    api.get('/analytics/streaks'),
  getHistory: (limit = 50) => 
    api.get(`/analytics/history?limit=${limit}`),
};

export default api;
