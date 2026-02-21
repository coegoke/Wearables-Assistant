/**
 * Message Component - Individual message with tool calls display
 */
import { useState } from 'react';
import { User, Bot, ChevronDown, ChevronUp, Wrench } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { formatDistanceToNow } from 'date-fns';
import './Message.css';

function Message({ message }) {
  const [showTools, setShowTools] = useState(false);
  const isUser = message.role === 'user';
  const hasToolCalls = message.tool_calls && message.tool_calls.length > 0;

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-avatar">
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      
      <div className="message-body">
        <div className="message-header">
          <span className="message-role">
            {isUser ? 'You' : 'Assistant'}
          </span>
          {message.timestamp && (
            <span className="message-time">
              {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
            </span>
          )}
        </div>
        
        <div className="message-content">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {/* Tool Calls Display */}
        {hasToolCalls && (
          <div className="tool-calls-section">
            <button
              className="tool-toggle"
              onClick={() => setShowTools(!showTools)}
            >
              <Wrench size={14} />
              <span>{message.tool_calls.length} tool{message.tool_calls.length > 1 ? 's' : ''} used</span>
              {showTools ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>

            {showTools && (
              <div className="tool-calls-list">
                {message.tool_calls.map((tool, index) => (
                  <div key={index} className="tool-call-item">
                    <div className="tool-call-header">
                      <span className="tool-name">{tool.tool_name}</span>
                    </div>
                    
                    {tool.arguments && Object.keys(tool.arguments).length > 0 && (
                      <div className="tool-section">
                        <div className="tool-section-title">Arguments:</div>
                        <pre className="tool-code">
                          {JSON.stringify(tool.arguments, null, 2)}
                        </pre>
                      </div>
                    )}
                    
                    {tool.result && (
                      <div className="tool-section">
                        <div className="tool-section-title">Result:</div>
                        <div className="tool-result">
                          {tool.result}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;
