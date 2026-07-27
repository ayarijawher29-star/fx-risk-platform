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
    <div className="card-glass">
      <h2 style={{ margin: '0 0 20px 0', fontSize: '18px' }}>🛡️ Module Client (Sales)</h2>

      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '12px' }}>
        <div>
          <label className="field-label">Montant</label>
          <input
            type="number"
            value={form.amount}
            onChange={e => setForm({ ...form, amount: Number(e.target.value) })}
            className="field-input"
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div>
            <label className="field-label">Devise</label>
            <select
              value={form.currency}
              onChange={e => setForm({ ...form, currency: e.target.value })}
              className="field-input"
            >
              <option value="EUR">EUR</option>
              <option value="USD">USD</option>
            </select>
          </div>

          <div>
            <label className="field-label">Échéance (mois)</label>
            <select
              value={form.maturity_months}
              onChange={e => setForm({ ...form, maturity_months: Number(e.target.value) })}
              className="field-input"
            >
              <option value={1}>1 mois</option>
              <option value={3}>3 mois</option>
              <option value={6}>6 mois</option>
              <option value={12}>12 mois</option>
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div>
            <label className="field-label">Statut</label>
            <select
              value={form.status}
              onChange={e => setForm({ ...form, status: e.target.value })}
              className="field-input"
            >
              <option value="firm">Engagement ferme</option>
              <option value="forecast">Prévision</option>
            </select>
          </div>

          <div>
            <label className="field-label">Type de flux</label>
            <select
              value={form.flow_type}
              onChange={e => setForm({ ...form, flow_type: e.target.value })}
              className="field-input"
            >
              <option value="importer">Importateur (achat)</option>
              <option value="exporter">Exportateur (vente)</option>
            </select>
          </div>
        </div>

        <div>
          <label className="field-label">Taux budgété</label>
          <input
            type="number"
            step="0.0001"
            value={form.budget_rate}
            onChange={e => setForm({ ...form, budget_rate: Number(e.target.value) })}
            className="field-input"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '12px',
            borderRadius: '8px',
            border: 'none',
            background: 'linear-gradient(135deg, var(--accent-blue), var(--accent-cyan))',
            color: 'white',
            fontWeight: 'bold',
            cursor: 'pointer',
            marginTop: '8px'
          }}
        >
          {loading ? 'Analyse...' : 'Analyser la couverture'}
        </button>
      </form>

      {result && (
        <div className="card" style={{ marginTop: '20px', padding: '15px' }}>
          <h3
            style={{
              margin: '0 0 12px 0',
              fontSize: '14px',
              color: 'var(--accent-blue)',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
            Résultat de l'analyse
          </h3>

          <div style={{ display: 'grid', gap: '10px', fontSize: '13px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-green)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="1" x2="12" y2="23" />
                <path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6" />
              </svg>
              <span><strong>Montant à couvrir :</strong> {result.montant_a_couvrir.toLocaleString()}</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-blue)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="20" x2="18" y2="10" />
                <line x1="12" y1="20" x2="12" y2="4" />
                <line x1="6" y1="20" x2="6" y2="14" />
              </svg>
              <span><strong>Position dans la bande :</strong> {result.pct_dans_bande}</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              <span><strong>Instrument :</strong> {result.instrument}</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-cyan)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="17 1 21 5 17 9" />
                <path d="M3 11V9a4 4 0 014-4h14" />
                <polyline points="7 23 3 19 7 15" />
                <path d="M21 13v2a4 4 0 01-4 4H3" />
              </svg>
              <span><strong>Taux à terme :</strong> {result.taux_a_terme}</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent-gold)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 6v6l4 2" />
              </svg>
              <span><strong>Coût :</strong> {result.cout_couverture.toLocaleString()}</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke={result.ecart_vs_budget > 0 ? 'var(--accent-red)' : 'var(--accent-green)'}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <polyline points={result.ecart_vs_budget > 0 ? '23 6 13.5 15.5 8.5 10.5 1 18' : '23 18 13.5 8.5 8.5 13.5 1 6'} />
                <polyline points={result.ecart_vs_budget > 0 ? '17 6 23 6 23 12' : '17 18 23 18 23 12'} />
              </svg>
              <span><strong>Écart vs budget :</strong> {result.ecart_vs_budget > 0 ? '+' : ''}{result.ecart_vs_budget}</span>
            </div>

            <div
              style={{
                marginTop: '4px',
                padding: '10px',
                background: 'var(--bg-secondary)',
                borderRadius: '6px',
                borderLeft: '3px solid var(--accent-blue)',
                fontStyle: 'italic',
                color: 'var(--text-secondary)'
              }}
            >
              {result.justification}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientForm;