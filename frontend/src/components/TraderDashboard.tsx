import React, { useEffect, useState } from 'react';
import { getTraderBook } from '../services/api';

interface TraderData {
  position_nette: number;
  limite_var: number;
  var_actuelle: number;
  utilisation_pct: number;
  montant_a_couvrir: number;
  risque_residuel: number;
  instrument_recommande: string;
  depassement: boolean;
  timing_signal: string | null;
  volatilite: number;
}

const TraderDashboard: React.FC = () => {
  const [data, setData] = useState<Record<string, TraderData> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getTraderBook();
        setData(response.data);
      } catch (err) {
        setError('Impossible de récupérer les données du book. Vérifiez que le backend tourne.');
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  if (loading) return <div style={{ color: 'white', textAlign: 'center', padding: '40px' }}>Chargement...</div>;
  if (error) return <div style={{ color: '#ef4444', textAlign: 'center', padding: '40px' }}>{error}</div>;
  if (!data) return null;

  return (
    <div style={{ display: 'grid', gap: '16px' }}>
      {Object.entries(data).map(([currency, info]) => (
        <div key={currency} style={{
          background: '#1e293b',
          borderRadius: '12px',
          padding: '20px',
          color: 'white',
          fontFamily: 'system-ui',
          borderLeft: info.depassement ? '4px solid #ef4444' : '4px solid #22c55e'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h3 style={{ margin: 0, fontSize: '18px' }}>💱 {currency}</h3>
            <span style={{
              padding: '4px 12px',
              borderRadius: '20px',
              fontSize: '12px',
              fontWeight: 'bold',
              background: info.depassement ? '#ef4444' : '#22c55e',
              color: 'white'
            }}>
              {info.depassement ? '⚠️ DÉPASSEMENT' : '✅ CONFORME'}
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '14px' }}>
            <div>
              <div style={{ color: '#94a3b8', fontSize: '12px' }}>Position nette</div>
              <div style={{ fontWeight: 'bold', fontSize: '16px' }}>{info.position_nette.toLocaleString()}</div>
            </div>
            <div>
              <div style={{ color: '#94a3b8', fontSize: '12px' }}>VaR actuelle</div>
              <div style={{ fontWeight: 'bold', fontSize: '16px' }}>{info.var_actuelle.toLocaleString()}</div>
            </div>
            <div>
              <div style={{ color: '#94a3b8', fontSize: '12px' }}>Limite VaR</div>
              <div>{info.limite_var.toLocaleString()}</div>
            </div>
            <div>
              <div style={{ color: '#94a3b8', fontSize: '12px' }}>Utilisation</div>
              <div style={{ color: info.utilisation_pct > 80 ? '#ef4444' : '#22c55e' }}>
                {info.utilisation_pct}%
              </div>
            </div>
            <div>
              <div style={{ color: '#94a3b8', fontSize: '12px' }}>Montant à couvrir</div>
              <div style={{ color: info.montant_a_couvrir > 0 ? '#ef4444' : '#94a3b8' }}>
                {info.montant_a_couvrir.toLocaleString()}
              </div>
            </div>
            <div>
              <div style={{ color: '#94a3b8', fontSize: '12px' }}>Instrument</div>
              <div>{info.instrument_recommande}</div>
            </div>
          </div>

          {info.timing_signal && (
            <div style={{ marginTop: '12px', padding: '8px', background: '#0f172a', borderRadius: '6px', fontSize: '13px' }}>
              📡 Signal timing : <strong>{info.timing_signal}</strong> | Volatilité : {info.volatilite}%
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default TraderDashboard;