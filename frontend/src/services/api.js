/**
 * API Service - handles all backend communication
 */
import axios from 'axios';

const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatAPI = {
  sendMessage: async (channelId, message) => {
    const response = await api.post('/chat/message', {
      channel_id: channelId,
      message,
    });
    return response.data;
  },

  getHistory: async (channelId) => {
    const response = await api.get(`/chat/history/${channelId}`);
    return response.data;
  },

  clearHistory: async (channelId) => {
    const response = await api.delete(`/chat/history/${channelId}`);
    return response.data;
  },
};

// Channel API
export const channelAPI = {
  list: async () => {
    const response = await api.get('/channels/');
    return response.data;
  },

  create: async (name) => {
    const response = await api.post('/channels/', { name });
    return response.data;
  },

  get: async (channelId) => {
    const response = await api.get(`/channels/${channelId}`);
    return response.data;
  },

  delete: async (channelId) => {
    const response = await api.delete(`/channels/${channelId}`);
    return response.data;
  },
};

// Graph API
export const graphAPI = {
  getGraph: async () => {
    const response = await api.get('/graph/');
    return response.data;
  },
};

// Health Check
export const healthAPI = {
  check: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
