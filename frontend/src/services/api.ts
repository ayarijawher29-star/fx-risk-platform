import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getEURUSDHistory = () => api.get('/market/eurusd');
export const getTNDFixing = () => api.get('/market/tnd');
export const getMacroSummary = () => api.get('/market/macro');
export const getSignal = (pair: string) => api.get(`/signal/${pair}`);
export const getTraderBook = () => api.get('/trader/book');

export interface ClientRequest {
  amount: number;
  currency: string;
  maturity_months: number;
  status: string;
  budget_rate: number;
  flow_type: string;
}

export const analyzeClient = (data: ClientRequest) => api.post('/client/analyze', data);