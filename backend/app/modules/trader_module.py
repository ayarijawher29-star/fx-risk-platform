import json
import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import ClientExposure, MarketData
from app.engine.combiner import combined_signal

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


def load_limits():
    with open("../data/policy/limits.json", "r") as f:
        return json.load(f)


def get_historical_volatility(pair: str = "EURUSD", days: int = 20) -> float:
    """Calcule la volatilité historique annualisée."""
    session = SessionLocal()
    rows = session.query(MarketData).filter(
        MarketData.pair == pair
    ).order_by(MarketData.date.desc()).limit(days + 1).all()
    session.close()
    
    if len(rows) < 2:
        return 0.10  # Fallback 10%
    
    # Calcul des rendements logarithmiques
    returns = []
    prices = [r.close for r in reversed(rows)]
    for i in range(1, len(prices)):
        ret = math.log(prices[i] / prices[i-1])
        returns.append(ret)
    
    # Écart-type des rendements
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / len(returns)
    daily_vol = math.sqrt(variance)
    
    # Annualiser (sqrt(252))
    annual_vol = daily_vol * math.sqrt(252)
    return annual_vol


def compute_var_parametric(position: float, volatility: float, confidence: float = 0.95) -> float:
    """
    VaR paramétrique simplifiée.
    position: montant net en devise
    volatility: volatilité annualisée
    confidence: 0.95 = 95%
    """
    # Z-score pour 95%
    z_score = 1.645
    
    # VaR 1 jour
    daily_vol = volatility / math.sqrt(252)
    var = abs(position) * daily_vol * z_score
    
    return round(var, 2)


def aggregate_positions() -> dict:
    """Agrège toutes les positions clients en position nette trader."""
    session = SessionLocal()
    exposures = session.query(ClientExposure).all()
    session.close()
    
    positions = {"EUR": 0.0, "USD": 0.0}
    
    for exp in exposures:
        # Client achète = trader vend (position négative)
        # Client vend = trader achète (position positive)
        if exp.flow_type == "importer":
            # Client achète devise étrangère
            positions[exp.currency] -= exp.amount
        else:
            # Client vend devise étrangère
            positions[exp.currency] += exp.amount
    
    return positions


def process_trader_book() -> dict:
    """
    Logique métier complète du module trader.
    """
    limits = load_limits()
    positions = aggregate_positions()
    
    results = {}
    
    for currency, net_amount in positions.items():
        if currency == "EUR":
            pair = "EURUSD"
            var_limit = limits.get("trader_var_limit_eur", 50000)
        else:
            pair = "USDTND"
            var_limit = limits.get("trader_var_limit_usd", 50000)
        
        # Calcul VaR
        vol = get_historical_volatility(pair)
        current_var = compute_var_parametric(net_amount, vol)
        
        # Dépassement ?
        breach = current_var > var_limit
        utilization = (current_var / var_limit) * 100 if var_limit > 0 else 0
        
        # Action recommandée
        if breach:
            amount_to_hedge = current_var - var_limit
            # Spot si ponctuel, Swap si position récurrente
            instrument = "Swap" if abs(net_amount) > 1000000 else "Spot"
            residual_risk = current_var - amount_to_hedge
        else:
            amount_to_hedge = 0.0
            instrument = "Aucune action"
            residual_risk = current_var
        
        # Signal pour timing (EUR/USD uniquement)
        timing_signal = None
        if currency == "EUR":
            sig = combined_signal("EURUSD")
            timing_signal = sig["final_signal"]
        
        results[currency] = {
            "position_nette": round(net_amount, 2),
            "limite_var": var_limit,
            "var_actuelle": current_var,
            "utilisation_pct": round(utilization, 1),
            "montant_a_couvrir": round(amount_to_hedge, 2),
            "risque_residuel": round(residual_risk, 2),
            "instrument_recommande": instrument,
            "depassement": breach,
            "timing_signal": timing_signal,
            "volatilite": round(vol * 100, 2)  # en %
        }
    
    return results


if __name__ == "__main__":
    import json as _json
    
    print("=" * 50)
    print("MODULE TRADER - État du Book")
    print("=" * 50)
    
    book = process_trader_book()
    
    for currency, data in book.items():
        print(f"\n📊 DEVISE : {currency}")
        print(f"  Position nette     : {data['position_nette']:,.2f}")
        print(f"  Limite VaR         : {data['limite_var']:,.2f}")
        print(f"  VaR actuelle       : {data['var_actuelle']:,.2f}")
        print(f"  Utilisation        : {data['utilisation_pct']}%")
        print(f"  Dépassement        : {'OUI ⚠️' if data['depassement'] else 'Non ✅'}")
        print(f"  Montant à couvrir  : {data['montant_a_couvrir']:,.2f}")
        print(f"  Risque résiduel    : {data['risque_residuel']:,.2f}")
        print(f"  Instrument         : {data['instrument_recommande']}")
        print(f"  Volatilité (ann.)  : {data['volatilite']}%")
        if data['timing_signal']:
            print(f"  Timing signal      : {data['timing_signal']}")