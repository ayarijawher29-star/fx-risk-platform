import React, { useEffect, useState } from 'react';
import { getMacroSummary } from '../services/api';

interface MacroData {
  date: string;
  country: string;
  indicator: string;
  value: number;
}

const INDICATOR_LABELS: Record<string, { label: string; unit: string }> = {
  FED_RATE: { label: 'Taux Fed', unit: '%' },
  CPI: { label: 'Inflation US', unit: 'index' },
  NFP: { label: 'Emploi (NFP)', unit: 'k' },
  GDP: { label: 'PIB US', unit: 'B$' },
  UNEMPLOYMENT: { label: 'Chômage', unit: '%' },
};

const MacroDashboard: React.FC = () => {
  const [data, setData] = useState<MacroData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getMacroSummary();
        // Garder le dernier de chaque indicateur
        const latest: Record<string, MacroData> = {};
        response.data.indicators.forEach((item: MacroData) => {
          const key = `${item.country}-${item.indicator}`;
          if (!latest[key] || new Date(item.date) > new Date(latest[key].date)) {
            latest[key] = item;
          }
        });
        setData(Object.values(latest));
      } catch (err) {
        console.error('Erreur macro:', err);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  if (loading) return <div style={{ color: '#94a3b8', textAlign: 'center', padding: '20px' }}>Chargement macro...</div>;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
      {data.map((item, idx) => {
        const meta = INDICATOR_LABELS[item.indicator] || { label: item.indicator, unit: '' };
        const isHigh = item.indicator === 'FED_RATE' && item.value >= 5;
        const isLow = item.indicator === 'UNEMPLOYMENT' && item.value <= 4;
        
        return (
          <div key={idx} style={{
            background: '#1e293b',
            borderRadius: '10px',
            padding: '16px',
            color: 'white',
            borderTop: `3px solid ${item.country === 'US' ? '#3b82f6' : '#22c55e'}`
          }}>
            <div style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', marginBottom: '4px' }}>
              {item.country} • {meta.label}
            </div>
            <div style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '4px' }}>
              {item.value.toFixed(2)}{meta.unit}
            </div>
            <div style={{ fontSize: '11px', color: '#64748b' }}>
              {item.date}
            </div>
            {(isHigh || isLow) && (
              <div style={{ marginTop: '6px', fontSize: '11px', color: isHigh ? '#ef4444' : '#22c55e' }}>
                {isHigh ? '↑ Restrictif' : '↓ Solide'}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default MacroDashboard;