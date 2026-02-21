/**
 * Custom hooks for managing chat functionality
 */
import { useState, useCallback } from 'react';
import { chatAPI } from '../services/api';

export const useChat = (channelId) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (content) => {
    if (!content.trim() || !channelId) return;

    setIsLoading(true);
    setError(null);

    // Add user message optimistically
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await chatAPI.sendMessage(channelId, content);
      
      // Add assistant message with tool calls
      setMessages((prev) => [...prev, {
        ...response.message,
        tool_calls: response.tool_calls,
      }]);
    } catch (err) {
      setError(err.message || 'Failed to send message');
      // Remove optimistic user message on error
      setMessages((prev) => prev.filter((msg) => msg.id !== userMessage.id));
    } finally {
      setIsLoading(false);
    }
  }, [channelId]);

  const loadHistory = useCallback(async () => {
    if (!channelId) return;

    setIsLoading(true);
    try {
      const data = await chatAPI.getHistory(channelId);
      setMessages(data.messages || []);
    } catch (err) {
      setError(err.message || 'Failed to load history');
    } finally {
      setIsLoading(false);
    }
  }, [channelId]);

  const clearHistory = useCallback(async () => {
    if (!channelId) return;

    try {
      await chatAPI.clearHistory(channelId);
      setMessages([]);
    } catch (err) {
      setError(err.message || 'Failed to clear history');
    }
  }, [channelId]);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    loadHistory,
    clearHistory,
  };
};
