/**
 * ChatArea Component - Main chat interface
 */
import { useState, useEffect, useRef } from 'react';
import { Send, RotateCcw, Network } from 'lucide-react';
import { useChat } from '../hooks/useChat';
import MessageList from './MessageList';
import './ChatArea.css';

function ChatArea({ channel, channelId, onToggleGraph, showGraph }) {
  const [input, setInput] = useState('');
  const { messages, isLoading, sendMessage, loadHistory, clearHistory } = useChat(channelId);
  const textareaRef = useRef(null);

  // Load history when channel changes
  useEffect(() => {
    if (channelId) {
      loadHistory();
    }
  }, [channelId, loadHistory]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const message = input;
    setInput('');
    await sendMessage(message);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleClearHistory = async () => {
    if (confirm('Clear all messages in this channel?')) {
      await clearHistory();
    }
  };

  return (
    <div className="chat-area">
      {/* Header */}
      <header className="chat-header">
        <div className="channel-info">
          <h2>{channel?.name || 'Select a channel'}</h2>
          {channel && (
            <span className="message-count-badge">
              {channel.message_count} messages
            </span>
          )}
        </div>
        
        <div className="header-actions">
          <button
            className="icon-btn"
            onClick={handleClearHistory}
            title="Clear history"
            disabled={!channel || messages.length === 0}
          >
            <RotateCcw size={18} />
          </button>
          
          <button
            className={`icon-btn ${showGraph ? 'active' : ''}`}
            onClick={onToggleGraph}
            title="Toggle graph"
          >
            <Network size={18} />
          </button>
        </div>
      </header>

      {/* Messages */}
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Input Area */}
      <div className="input-area">
        <form onSubmit={handleSubmit} className="input-form">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={channel ? "Send a message..." : "Select a channel to start chatting"}
            disabled={!channel || isLoading}
            rows={1}
            maxLength={2000}
          />
          
          <button
            type="submit"
            className="send-btn"
            disabled={!channel || !input.trim() || isLoading}
            title="Send message"
          >
            <Send size={20} />
          </button>
        </form>
        
        <div className="input-footer">
          <p className="text-xs opacity-50">
            Ask about your wearables data - steps, sleep, heart rate, activities, and more
          </p>
        </div>
      </div>
    </div>
  );
}

export default ChatArea;
