import { useState } from 'react';
import { Shield, BarChart3, List } from 'lucide-react';
import Timer from './components/Timer';
import BlocklistManager from './components/BlocklistManager';
import Analytics from './components/Analytics';

function App() {
  const [activeTab, setActiveTab] = useState('timer');

  const tabs = [
    { id: 'timer', name: 'Focus Timer', icon: Shield },
    { id: 'blocklist', name: 'Blocklist', icon: List },
    { id: 'analytics', name: 'Analytics', icon: BarChart3 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-blue-500 rounded-xl">
                <Shield className="text-white" size={32} />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">FocusGuard</h1>
                <p className="text-gray-500 text-sm">Distraction-Free Productivity</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="flex gap-2 bg-white rounded-xl p-2 shadow-md">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-500 text-white shadow-md'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Icon size={20} />
                {tab.name}
              </button>
            );
          })}
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'timer' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Timer onSessionComplete={() => setActiveTab('analytics')} />
            <BlocklistManager />
          </div>
        )}
        
        {activeTab === 'blocklist' && (
          <div className="max-w-3xl mx-auto">
            <BlocklistManager />
          </div>
        )}
        
        {activeTab === 'analytics' && <Analytics />}
      </main>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center text-gray-500 text-sm">
        <p>Built with Python (Flask) + React | Innovation Phase Project</p>
      </footer>
    </div>
  );
}

export default App;
