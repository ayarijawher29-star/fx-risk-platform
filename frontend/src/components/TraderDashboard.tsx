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
  if (error) return <div style={{ color: 'var(--accent-red)', textAlign: 'center', padding: '40px' }}>{error}</div>;
  if (!data) return null;

  return (
    <div style={{ display: 'grid', gap: '16px' }}>
      {Object.entries(data).map(([currency, info]) => {
        const watch = !info.depassement && info.utilisation_pct > 60;
        return (
          <div key={currency} className="card" style={{
            borderLeft: info.depassement ? '4px solid var(--accent-red)' : watch ? '4px solid var(--accent-gold)' : '4px solid var(--accent-green)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <h3 style={{ margin: 0, fontSize: '18px' }}>💱 {currency}</h3>
              <span className={watch ? 'badge-gold' : ''} style={{
                padding: '4px 12px',
                borderRadius: '20px',
                fontSize: '12px',
                fontWeight: 'bold',
                background: info.depassement ? 'var(--accent-red)' : watch ? 'transparent' : 'var(--accent-green)',
                color: watch ? undefined : 'white'
              }}>
                {info.depassement ? '⚠️ DÉPASSEMENT' : watch ? '⚠ SURVEILLER' : '✅ CONFORME'}
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '14px' }}>
              <div>
                <div className="field-label">Position nette</div>
                <div style={{ fontWeight: 'bold', fontSize: '16px' }}>{info.position_nette.toLocaleString()}</div>
              </div>
              <div>
                <div className="field-label">VaR actuelle</div>
                <div style={{ fontWeight: 'bold', fontSize: '16px' }}>{info.var_actuelle.toLocaleString()}</div>
              </div>
              <div>
                <div className="field-label">Limite VaR</div>
                <div>{info.limite_var.toLocaleString()}</div>
              </div>
              <div>
                <div className="field-label">Utilisation</div>
                <div style={{ color: info.utilisation_pct > 80 ? 'var(--accent-red)' : 'var(--accent-green)' }}>
                  {info.utilisation_pct}%
                </div>
              </div>
              <div>
                <div className="field-label">Montant à couvrir</div>
                <div style={{ color: info.montant_a_couvrir > 0 ? 'var(--accent-red)' : 'var(--text-secondary)' }}>
                  {info.montant_a_couvrir.toLocaleString()}
                </div>
              </div>
              <div>
                <div className="field-label">Instrument</div>
                <div>{info.instrument_recommande}</div>
              </div>
            </div>

            {info.timing_signal && (
              <div style={{ marginTop: '12px', padding: '8px', background: 'var(--bg-secondary)', borderRadius: '6px', fontSize: '13px' }}>
                📡 Signal timing : <strong>{info.timing_signal}</strong> | Volatilité : {info.volatilite}%
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default TraderDashboard;