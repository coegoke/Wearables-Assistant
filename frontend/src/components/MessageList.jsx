/**
 * MessageList Component - Displays chat messages
 */
import { useEffect, useRef } from 'react';
import Message from './Message';
import './MessageList.css';

function MessageList({ messages, isLoading }) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="messages-container">
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h3>No messages yet</h3>
          <p>Start a conversation by sending a message below</p>
          <div className="example-queries">
            <p className="text-sm font-semibold">Try asking:</p>
            <ul>
              <li>"Show me my weekly summary"</li>
              <li>"How many steps did I take yesterday?"</li>
              <li>"What's my sleep quality this week?"</li>
              <li>"Show me my recent workouts"</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="messages-container">
      <div className="messages-list">
        {messages.map((message, index) => (
          <Message key={message.id || index} message={message} />
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

export default MessageList;
