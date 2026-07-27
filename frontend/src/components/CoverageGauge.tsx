import React from 'react';

interface GaugeProps {
  position: number;
  lowerBound: number;
  upperBound: number;
  currentSpot: number;
  label: string;
}

const CoverageGauge: React.FC<GaugeProps> = ({ position, lowerBound, upperBound, currentSpot, label }) => {
  const percentage = Math.round(position * 100);

  const getColor = () => {
    if (percentage <= 30) return 'var(--success)';
    if (percentage <= 70) return 'var(--warning)';
    return 'var(--danger)';
  };

  const getLabel = () => {
    if (percentage <= 30) return 'Attendre';
    if (percentage <= 70) return 'Neutre';
    return 'Couvrir vite';
  };

  return (
    <div style={{
      background: 'var(--bg-card)',
      borderRadius: '16px',
      padding: '24px',
      border: '1px solid var(--border-color)',
      boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between'
    }}>
      <div>
        <h3 style={{
          margin: '0 0 20px 0',
          fontSize: '13px',
          textTransform: 'uppercase',
          color: 'var(--text-secondary)',
          letterSpacing: '1px',
          fontWeight: '600'
        }}>
          {label}
        </h3>

        {/* Gauge Track */}
        <div style={{
          position: 'relative',
          height: '48px',
          background: 'linear-gradient(to right, var(--success), var(--warning), var(--danger))',
          borderRadius: '24px',
          overflow: 'hidden',
          opacity: 0.2,
          marginBottom: '8px'
        }} />

        {/* Gauge Marker */}
        <div style={{ position: 'relative', height: '4px', marginTop: '-32px', marginBottom: '28px' }}>
          <div style={{
            position: 'absolute',
            left: `${percentage}%`,
            transform: 'translate(-50%, -50%)',
            top: '50%',
            width: '28px',
            height: '28px',
            background: getColor(),
            borderRadius: '50%',
            border: '3px solid var(--bg-card)',
            boxShadow: `0 0 20px ${getColor()}40`,
            zIndex: 10,
            transition: 'all 0.5s ease'
          }} />
        </div>

        {/* Labels */}
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '16px' }}>
          <span>{lowerBound}</span>
          <span style={{ color: getColor(), fontWeight: '700', fontSize: '14px' }}>{percentage}% — {getLabel()}</span>
          <span>{upperBound}</span>
        </div>
      </div>

      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingTop: '16px',
        borderTop: '1px solid var(--border-color)'
      }}>
        <div>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Spot actuel</div>
          <div style={{ fontSize: '20px', fontWeight: '700', color: 'var(--text-primary)' }}>{currentSpot}</div>
        </div>
        <div style={{
          padding: '6px 14px',
          borderRadius: '20px',
          background: `${getColor()}15`,
          color: getColor(),
          fontSize: '12px',
          fontWeight: '600',
          border: `1px solid ${getColor()}30`
        }}>
          {percentage <= 30 ? 'Zone verte' : percentage <= 70 ? 'Zone jaune' : 'Zone rouge'}
        </div>
      </div>
    </div>
  );
};

export default CoverageGauge;