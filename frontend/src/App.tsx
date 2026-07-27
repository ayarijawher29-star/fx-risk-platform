import { useState } from 'react';
import ClientForm from './components/ClientForm';
import CoverageGauge from './components/CoverageGauge';
import TraderDashboard from './components/TraderDashboard';
import FXChart from './components/FXChart';
import MacroDashboard from './components/MacroDashboard';

function App() {
  const [activeTab, setActiveTab] = useState<'client' | 'trader'>('client');

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <header style={{
        background: 'linear-gradient(135deg, var(--bg-secondary) 0%, #0f172a 100%)',
        borderBottom: '1px solid var(--border-color)',
        padding: '24px 0',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        backdropFilter: 'blur(10px)'
      }}>
        <div className="page-container">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '4px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              background: 'linear-gradient(135deg, var(--accent-blue), var(--accent-cyan))',
              borderRadius: '10px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px'
            }}>
              🛡️
            </div>
            <div>
              <h1 style={{ margin: 0, fontSize: '22px', fontWeight: '700', color: 'var(--text-primary)', letterSpacing: '-0.5px' }}>
                FX Risk Management Platform
              </h1>
              <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-secondary)', fontWeight: '500' }}>
                Salle des marchés — Module Sales & Trader
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="page-container" style={{ padding: '24px' }}>
        <div style={{
          display: 'inline-flex',
          background: 'var(--bg-secondary)',
          borderRadius: '12px',
          padding: '4px',
          border: '1px solid var(--border-color)',
          gap: '4px'
        }}>
          <button
            onClick={() => setActiveTab('client')}
            style={{
              padding: '10px 24px',
              borderRadius: '10px',
              border: 'none',
              background: activeTab === 'client' ? 'linear-gradient(135deg, var(--accent-blue), var(--accent-cyan))' : 'transparent',
              color: 'white',
              fontWeight: '600',
              fontSize: '14px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: activeTab === 'client' ? '0 4px 14px rgba(59, 130, 246, 0.4)' : 'none'
            }}
          >
            🛡️ Module Client
          </button>
          <button
            onClick={() => setActiveTab('trader')}
            style={{
              padding: '10px 24px',
              borderRadius: '10px',
              border: 'none',
              background: activeTab === 'trader' ? 'linear-gradient(135deg, var(--accent-blue), var(--accent-cyan))' : 'transparent',
              color: 'white',
              fontWeight: '600',
              fontSize: '14px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: activeTab === 'trader' ? '0 4px 14px rgba(59, 130, 246, 0.4)' : 'none'
            }}
          >
            📊 Module Trader
          </button>
        </div>
      </div>

      <main className="page-container" style={{ paddingBottom: '24px' }}>
        {activeTab === 'client' && (
          <div className="animate-fade-in">
            <div className="grid-2" style={{ marginBottom: '20px' }}>
              <CoverageGauge
                position={0.75}
                lowerBound={3.30}
                upperBound={3.50}
                currentSpot={3.452}
                label="EUR/TND — Bande de couverture (3 mois)"
              />
              <div className="card-glass">
                <h3 className="card-title">📊 Contexte Marché</h3>
                <MacroDashboard />
              </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <FXChart />
            </div>

            <ClientForm />
          </div>
        )}

        {activeTab === 'trader' && (
          <div className="animate-fade-in">
            <div className="card-glass" style={{ marginBottom: '20px' }}>
              <h2 style={{ margin: '0 0 20px 0', fontSize: '18px', fontWeight: '600', color: 'var(--text-primary)' }}>
                📊 Module Trader — Gestion du Book
              </h2>
              <TraderDashboard />
            </div>
          </div>
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '40px 24px',
        color: 'var(--text-muted)',
        fontSize: '12px',
        borderTop: '1px solid var(--border-color)',
        marginTop: '40px'
      }}>
        <p>FX Risk Platform — Outil de démonstration de gestion de risque de change</p>
        <p style={{ marginTop: '4px' }}>Données simulées à des fins pédagogiques</p>
      </footer>
    </div>
  );
}

export default App;