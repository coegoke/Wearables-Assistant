/**
 * Main App Component
 */
import { useState } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import GraphPanel from './components/GraphPanel';
import { useChannels } from './hooks/useChannels';

function App() {
  const {
    channels,
    activeChannel,
    activeChannelId,
    createChannel,
    deleteChannel,
    selectChannel,
  } = useChannels();

  const [showGraph, setShowGraph] = useState(true);

  return (
    <div className="app">
      <Sidebar
        channels={channels}
        activeChannelId={activeChannelId}
        onChannelSelect={selectChannel}
        onChannelCreate={createChannel}
        onChannelDelete={deleteChannel}
      />
      
      <main className="main-content">
        <ChatArea
          channel={activeChannel}
          channelId={activeChannelId}
          onToggleGraph={() => setShowGraph(!showGraph)}
          showGraph={showGraph}
        />
      </main>

      {showGraph && (
        <GraphPanel onClose={() => setShowGraph(false)} />
      )}
    </div>
  );
}

export default App;
