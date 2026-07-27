import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getEURUSDHistory } from '../services/api';

interface ChartData {
  date: string;
  close: number;
  sma50?: number;
  sma100?: number;
  bbUpper?: number;
  bbLower?: number;
}

const FXChart: React.FC = () => {
  const [data, setData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getEURUSDHistory();
        const raw = response.data.data;

        const processed = raw.map((item: any, index: number, arr: any[]) => {
          const window50 = arr.slice(Math.max(0, index - 49), index + 1);
          const window100 = arr.slice(Math.max(0, index - 99), index + 1);
          const window20 = arr.slice(Math.max(0, index - 19), index + 1);

          const sma50 = window50.length >= 50
            ? window50.reduce((sum: number, r: any) => sum + r.close, 0) / window50.length
            : null;
          const sma100 = window100.length >= 100
            ? window100.reduce((sum: number, r: any) => sum + r.close, 0) / window100.length
            : null;

          let bbUpper = null, bbLower = null;
          if (window20.length >= 20) {
            const mean = window20.reduce((sum: number, r: any) => sum + r.close, 0) / window20.length;
            const variance = window20.reduce((sum: number, r: any) => sum + Math.pow(r.close - mean, 2), 0) / window20.length;
            const std = Math.sqrt(variance);
            bbUpper = mean + (std * 2);
            bbLower = mean - (std * 2);
          }

          return {
            date: item.date.slice(5),
            close: item.close,
            sma50,
            sma100,
            bbUpper,
            bbLower
          };
        });

        setData(processed.slice(-90));
      } catch (err) {
        console.error('Erreur chargement graphique:', err);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  if (loading) return <div style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '40px' }}>Chargement du graphique...</div>;

  return (
    <div className="card-glass">
      <h3 className="card-title" style={{ fontSize: '16px' }}>📈 EUR/USD — 90 derniers jours</h3>
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
          <XAxis dataKey="date" stroke="var(--text-secondary)" fontSize={12} />
          <YAxis domain={['auto', 'auto']} stroke="var(--text-secondary)" fontSize={12} />
          <Tooltip
            contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'white' }}
          />
          <Legend />
          <Line type="monotone" dataKey="close" stroke="var(--accent-blue)" strokeWidth={2} dot={false} name="Prix" />
          <Line type="monotone" dataKey="sma50" stroke="var(--accent-green)" strokeWidth={1} dot={false} name="SMA 50" />
          <Line type="monotone" dataKey="sma100" stroke="var(--accent-gold)" strokeWidth={1} dot={false} name="SMA 100" />
          <Line type="monotone" dataKey="bbUpper" stroke="var(--accent-red)" strokeWidth={1} dot={false} strokeDasharray="5 5" name="BB Upper" />
          <Line type="monotone" dataKey="bbLower" stroke="var(--accent-red)" strokeWidth={1} dot={false} strokeDasharray="5 5" name="BB Lower" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default FXChart;