/**
 * Sidebar Component - Channel list and management
 */
import { useState } from 'react';
import { Plus, MessageSquare, Trash2, Activity } from 'lucide-react';
import './Sidebar.css';

function Sidebar({ channels, activeChannelId, onChannelSelect, onChannelCreate, onChannelDelete }) {
  const [isCreating, setIsCreating] = useState(false);
  const [newChannelName, setNewChannelName] = useState('');

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newChannelName.trim()) return;

    try {
      await onChannelCreate(newChannelName);
      setNewChannelName('');
      setIsCreating(false);
    } catch (err) {
      console.error('Failed to create channel:', err);
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <Activity size={24} />
          <h1>Wearables AI</h1>
        </div>
        
        <button
          className="new-chat-btn"
          onClick={() => setIsCreating(true)}
          title="New Channel"
        >
          <Plus size={20} />
          <span>New Channel</span>
        </button>
      </div>

      {isCreating && (
        <form className="channel-form" onSubmit={handleCreate}>
          <input
            type="text"
            placeholder="Channel name..."
            value={newChannelName}
            onChange={(e) => setNewChannelName(e.target.value)}
            autoFocus
            maxLength={50}
          />
          <div className="form-actions">
            <button type="submit" className="btn-primary">
              Create
            </button>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => {
                setIsCreating(false);
                setNewChannelName('');
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="channel-list">
        {channels.map((channel) => (
          <div
            key={channel.id}
            className={`channel-item ${channel.id === activeChannelId ? 'active' : ''}`}
            onClick={() => onChannelSelect(channel.id)}
          >
            <MessageSquare size={16} />
            <span className="channel-name truncate">{channel.name}</span>
            <span className="message-count">{channel.message_count}</span>
            {channels.length > 1 && (
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  if (confirm(`Delete channel "${channel.name}"?`)) {
                    onChannelDelete(channel.id);
                  }
                }}
                title="Delete channel"
              >
                <Trash2 size={14} />
              </button>
            )}
          </div>
        ))}
      </div>

      <div className="sidebar-footer">
        <div className="info-text text-xs opacity-50">
          Powered by LangGraph & Groq
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
