import { useState } from 'react';
import ClientForm from './components/ClientForm';
import CoverageGauge from './components/CoverageGauge';
import TraderDashboard from './components/TraderDashboard';
import FXChart from './components/FXChart';
import MacroDashboard from './components/MacroDashboard';

function App() {
  const [activeTab, setActiveTab] = useState<'client' | 'trader'>('client');

  return (
    <div style={{ minHeight: '100vh', background: '#0f172a', padding: '20px', fontFamily: 'system-ui, sans-serif' }}>
      {/* Header */}
      <header style={{ textAlign: 'center', marginBottom: '30px' }}>
        <h1 style={{ color: 'white', margin: 0, fontSize: '28px' }}>FX Risk Management Platform</h1>
        <p style={{ color: '#94a3b8', margin: '8px 0 0 0', fontSize: '14px' }}>
          Plateforme d'aide à la décision de couverture FX
        </p>
      </header>

      {/* Navigation */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginBottom: '20px' }}>
        <button 
          onClick={() => setActiveTab('client')}
          style={{
            padding: '10px 24px',
            borderRadius: '8px',
            border: 'none',
            background: activeTab === 'client' ? '#3b82f6' : '#334155',
            color: 'white',
            fontWeight: 'bold',
            cursor: 'pointer'
          }}
        >
          🛡️ Module Client
        </button>
        <button 
          onClick={() => setActiveTab('trader')}
          style={{
            padding: '10px 24px',
            borderRadius: '8px',
            border: 'none',
            background: activeTab === 'trader' ? '#3b82f6' : '#334155',
            color: 'white',
            fontWeight: 'bold',
            cursor: 'pointer'
          }}
        >
          📊 Module Trader
        </button>
      </div>

      {/* Content */}
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        {activeTab === 'client' && (
          <div>
            <div style={{ marginBottom: '20px' }}>
              <CoverageGauge 
                position={0.75} 
                lowerBound={3.30} 
                upperBound={3.50} 
                currentSpot={3.452} 
                label="EUR/TND — Bande de couverture (3 mois)"
              />
            </div>
            <div style={{ marginBottom: '20px' }}>
              <FXChart />
            </div>
            <div style={{ marginBottom: '20px' }}>
              <MacroDashboard />
            </div>
            <ClientForm />
          </div>
        )}
        
        {activeTab === 'trader' && (
          <div>
            <h2 style={{ color: 'white', textAlign: 'center', marginBottom: '20px' }}>📊 Module Trader (Book)</h2>
            <TraderDashboard />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;