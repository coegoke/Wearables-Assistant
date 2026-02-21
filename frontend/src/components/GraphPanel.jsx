/**
 * GraphPanel Component - LangGraph visualization in sidebar
 */
import { useEffect, useState } from 'react';
import { X, RefreshCw } from 'lucide-react';
import { graphAPI } from '../services/api';
import mermaid from 'mermaid';
import './GraphPanel.css';

// Initialize mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#10a37f',
    primaryTextColor: '#ececf1',
    primaryBorderColor: '#565869',
    lineColor: '#8e8ea0',
    secondaryColor: '#40414f',
    tertiaryColor: '#202123',
  },
});

function GraphPanel({ onClose }) {
  const [graphData, setGraphData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [view, setView] = useState('diagram'); // 'diagram' or 'image'

  const loadGraph = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await graphAPI.getGraph();
      setGraphData(data);
      
      // Render mermaid diagram
      if (data.mermaid && view === 'diagram') {
        setTimeout(() => {
          renderMermaid(data.mermaid);
        }, 100);
      }
    } catch (err) {
      setError(err.message || 'Failed to load graph');
    } finally {
      setIsLoading(false);
    }
  };

  const renderMermaid = async (mermaidCode) => {
    const element = document.getElementById('mermaid-diagram');
    if (element) {
      try {
        element.innerHTML = mermaidCode;
        await mermaid.run({
          querySelector: '#mermaid-diagram',
        });
      } catch (err) {
        console.error('Mermaid render error:', err);
      }
    }
  };

  useEffect(() => {
    loadGraph();
  }, []);

  useEffect(() => {
    if (graphData?.mermaid && view === 'diagram') {
      renderMermaid(graphData.mermaid);
    }
  }, [view, graphData]);

  return (
    <aside className="graph-panel">
      <div className="graph-header">
        <h3>Workflow Graph</h3>
        <div className="graph-actions">
          <button
            className="icon-btn"
            onClick={loadGraph}
            title="Refresh graph"
            disabled={isLoading}
          >
            <RefreshCw size={16} className={isLoading ? 'spin' : ''} />
          </button>
          <button
            className="icon-btn"
            onClick={onClose}
            title="Close panel"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      <div className="graph-content">
        {isLoading && (
          <div className="graph-loading">
            <div className="spinner"></div>
            <p>Loading graph...</p>
          </div>
        )}

        {error && (
          <div className="graph-error">
            <p>⚠️ {error}</p>
            <button onClick={loadGraph}>Retry</button>
          </div>
        )}

        {!isLoading && !error && graphData && (
          <>
            {/* View Toggle */}
            <div className="view-toggle">
              <button
                className={view === 'diagram' ? 'active' : ''}
                onClick={() => setView('diagram')}
              >
                Diagram
              </button>
              {graphData.png_base64 && (
                <button
                  className={view === 'image' ? 'active' : ''}
                  onClick={() => setView('image')}
                >
                  Image
                </button>
              )}
            </div>

            {/* Graph Display */}
            {view === 'diagram' && graphData.mermaid && (
              <div className="mermaid-container">
                <div id="mermaid-diagram" className="mermaid"></div>
              </div>
            )}

            {view === 'image' && graphData.png_base64 && (
              <div className="image-container">
                <img
                  src={`data:image/png;base64,${graphData.png_base64}`}
                  alt="Workflow Graph"
                />
              </div>
            )}

            {/* Graph Info */}
            <div className="graph-info">
              <h4>How it works:</h4>
              <ul>
                <li><strong>Agent:</strong> Processes user input and decides actions</li>
                <li><strong>Tools:</strong> Executes database queries</li>
                <li><strong>Loop:</strong> Continues until answer is complete</li>
              </ul>
            </div>
          </>
        )}
      </div>
    </aside>
  );
}

export default GraphPanel;
