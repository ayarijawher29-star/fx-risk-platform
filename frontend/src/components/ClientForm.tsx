import React, { useState } from 'react';
import { analyzeClient } from '../services/api';
import type { ClientRequest } from '../services/api';

interface ClientResult {
  montant_a_couvrir: number;
  pct_dans_bande: string;
  instrument: string;
  taux_a_terme: number;
  cout_couverture: number;
  ecart_vs_budget: number;
  justification: string;
  meta: {
    spot: number;
    bande: string;
    coverage_pct: string;
  };
}

const ClientForm: React.FC = () => {
  const [form, setForm] = useState<ClientRequest>({
    amount: 500000,
    currency: 'EUR',
    maturity_months: 3,
    status: 'firm',
    budget_rate: 3.42,
    flow_type: 'importer'
  });
  
  const [result, setResult] = useState<ClientResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await analyzeClient(form);
      setResult(response.data);
    } catch (err) {
      alert('Erreur API. Vérifiez que le backend tourne sur le port 8000.');
    }
    setLoading(false);
  };

  return (
    <div style={{ background: '#1e293b', borderRadius: '12px', padding: '20px', color: 'white', fontFamily: 'system-ui' }}>
      <h2 style={{ margin: '0 0 20px 0', fontSize: '18px' }}>🛡️ Module Client (Sales)</h2>
      
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '12px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Montant</label>
          <input type="number" value={form.amount} onChange={e => setForm({...form, amount: Number(e.target.value)})}
            style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #475569', background: '#334155', color: 'white' }} />
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Devise</label>
            <select value={form.currency} onChange={e => setForm({...form, currency: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #475569', background: '#334155', color: 'white' }}>
              <option value="EUR">EUR</option>
              <option value="USD">USD</option>
            </select>
          </div>
          
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Échéance (mois)</label>
            <select value={form.maturity_months} onChange={e => setForm({...form, maturity_months: Number(e.target.value)})}
              style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #475569', background: '#334155', color: 'white' }}>
              <option value={1}>1 mois</option>
              <option value={3}>3 mois</option>
              <option value={6}>6 mois</option>
              <option value={12}>12 mois</option>
            </select>
          </div>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Statut</label>
            <select value={form.status} onChange={e => setForm({...form, status: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #475569', background: '#334155', color: 'white' }}>
              <option value="firm">Engagement ferme</option>
              <option value="forecast">Prévision</option>
            </select>
          </div>
          
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Type de flux</label>
            <select value={form.flow_type} onChange={e => setForm({...form, flow_type: e.target.value})}
              style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #475569', background: '#334155', color: 'white' }}>
              <option value="importer">Importateur (achat)</option>
              <option value="exporter">Exportateur (vente)</option>
            </select>
          </div>
        </div>
        
        <div>
          <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>Taux budgété</label>
          <input type="number" step="0.0001" value={form.budget_rate} onChange={e => setForm({...form, budget_rate: Number(e.target.value)})}
            style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #475569', background: '#334155', color: 'white' }} />
        </div>
        
        <button type="submit" disabled={loading}
          style={{ padding: '12px', borderRadius: '8px', border: 'none', background: '#3b82f6', color: 'white', fontWeight: 'bold', cursor: 'pointer', marginTop: '8px' }}>
          {loading ? 'Analyse...' : 'Analyser la couverture'}
        </button>
      </form>
      
      {result && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#0f172a', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3 style={{ margin: '0 0 12px 0', fontSize: '14px', color: '#60a5fa' }}>📋 Résultat</h3>
          <div style={{ display: 'grid', gap: '8px', fontSize: '13px' }}>
            <div>💰 <strong>Montant à couvrir :</strong> {result.montant_a_couvrir.toLocaleString()}</div>
            <div>📊 <strong>Position dans la bande :</strong> {result.pct_dans_bande}</div>
            <div>📜 <strong>Instrument :</strong> {result.instrument}</div>
            <div>💱 <strong>Taux à terme :</strong> {result.taux_a_terme}</div>
            <div>💸 <strong>Coût :</strong> {result.cout_couverture.toLocaleString()}</div>
            <div>📈 <strong>Écart vs budget :</strong> {result.ecart_vs_budget > 0 ? '+' : ''}{result.ecart_vs_budget}</div>
            <div style={{ marginTop: '8px', padding: '8px', background: '#1e293b', borderRadius: '4px', fontStyle: 'italic', color: '#cbd5e1' }}>
              "{result.justification}"
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientForm;