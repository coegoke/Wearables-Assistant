/**
 * Custom hook for managing channels
 */
import { useState, useCallback, useEffect } from 'react';
import { channelAPI } from '../services/api';

export const useChannels = () => {
  const [channels, setChannels] = useState([]);
  const [activeChannelId, setActiveChannelId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadChannels = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await channelAPI.list();
      setChannels(data.channels || []);
      
      // Set first channel as active if none selected
      if (!activeChannelId && data.channels.length > 0) {
        setActiveChannelId(data.channels[0].id);
      }
    } catch (err) {
      setError(err.message || 'Failed to load channels');
    } finally {
      setIsLoading(false);
    }
  }, [activeChannelId]);

  const createChannel = useCallback(async (name) => {
    try {
      const newChannel = await channelAPI.create(name);
      setChannels((prev) => [...prev, newChannel]);
      setActiveChannelId(newChannel.id);
      return newChannel;
    } catch (err) {
      setError(err.message || 'Failed to create channel');
      throw err;
    }
  }, []);

  const deleteChannel = useCallback(async (channelId) => {
    try {
      await channelAPI.delete(channelId);
      setChannels((prev) => prev.filter((ch) => ch.id !== channelId));
      
      // Switch to first available channel if active was deleted
      if (channelId === activeChannelId) {
        const remaining = channels.filter((ch) => ch.id !== channelId);
        setActiveChannelId(remaining.length > 0 ? remaining[0].id : null);
      }
    } catch (err) {
      setError(err.message || 'Failed to delete channel');
      throw err;
    }
  }, [channels, activeChannelId]);

  const selectChannel = useCallback((channelId) => {
    setActiveChannelId(channelId);
  }, []);

  const activeChannel = channels.find((ch) => ch.id === activeChannelId);

  // Load channels on mount
  useEffect(() => {
    loadChannels();
  }, []);

  return {
    channels,
    activeChannel,
    activeChannelId,
    isLoading,
    error,
    createChannel,
    deleteChannel,
    selectChannel,
    refreshChannels: loadChannels,
  };
};
