import React from 'react';

interface GaugeProps {
  position: number; // 0.0 to 1.0
  lowerBound: number;
  upperBound: number;
  currentSpot: number;
  label: string;
}

const CoverageGauge: React.FC<GaugeProps> = ({ position, lowerBound, upperBound, currentSpot, label }) => {
  const percentage = Math.round(position * 100);
  
  // Color based on position
  const getColor = () => {
    if (percentage <= 30) return '#22c55e'; // green - wait
    if (percentage <= 70) return '#eab308'; // yellow - neutral
    return '#ef4444'; // red - cover now
  };

  return (
    <div style={{ 
      background: '#1e293b', 
      borderRadius: '12px', 
      padding: '20px', 
      margin: '10px 0',
      color: 'white',
      fontFamily: 'system-ui, sans-serif'
    }}>
      <h3 style={{ margin: '0 0 15px 0', fontSize: '14px', textTransform: 'uppercase', color: '#94a3b8' }}>
        {label}
      </h3>
      
      {/* Gauge bar */}
      <div style={{ position: 'relative', height: '40px', background: '#334155', borderRadius: '20px', overflow: 'hidden' }}>
        {/* Gradient background */}
        <div style={{
          position: 'absolute',
          left: 0, right: 0, top: 0, bottom: 0,
          background: 'linear-gradient(to right, #22c55e 0%, #eab308 50%, #ef4444 100%)',
          opacity: 0.3
        }} />
        
        {/* Position marker */}
        <div style={{
          position: 'absolute',
          left: `${percentage}%`,
          top: '50%',
          transform: 'translate(-50%, -50%)',
          width: '24px',
          height: '24px',
          background: getColor(),
          borderRadius: '50%',
          border: '3px solid white',
          boxShadow: '0 0 10px rgba(0,0,0,0.5)',
          zIndex: 10
        }} />
        
        {/* Tick marks */}
        <div style={{ position: 'absolute', left: '25%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.2)' }} />
        <div style={{ position: 'absolute', left: '50%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.3)' }} />
        <div style={{ position: 'absolute', left: '75%', top: 0, bottom: 0, width: '2px', background: 'rgba(255,255,255,0.2)' }} />
      </div>
      
      {/* Labels */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '8px', fontSize: '12px', color: '#94a3b8' }}>
        <span>Attendre ({lowerBound})</span>
        <span style={{ fontWeight: 'bold', color: getColor(), fontSize: '14px' }}>{percentage}%</span>
        <span>Couvrir vite ({upperBound})</span>
      </div>
      
      <div style={{ marginTop: '10px', fontSize: '13px', color: '#cbd5e1' }}>
        Spot actuel : <strong>{currentSpot}</strong>
      </div>
    </div>
  );
};

export default CoverageGauge;