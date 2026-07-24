import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import FXFixingTND, MarketData
from app.engine.combiner import combined_signal

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


def load_policy():
    with open("../data/policy/bands.json", "r") as f:
        bands = json.load(f)
    with open("../data/policy/limits.json", "r") as f:
        limits = json.load(f)
    return bands, limits


def get_spot(pair: str):
    """Récupère le dernier spot disponible."""
    session = SessionLocal()
    try:
        if pair == "EURUSD":
            row = session.query(MarketData).filter(MarketData.pair == "EURUSD").order_by(MarketData.date.desc()).first()
            spot = row.close if row else 1.08
        else:
            row = session.query(FXFixingTND).order_by(FXFixingTND.date.desc()).first()
            if row:
                spot = row.eur_tnd if pair == "EURTND" else row.usd_tnd
            else:
                spot = 3.45 if pair == "EURTND" else 3.18
    finally:
        session.close()
    return spot


def get_band(pair: str, maturity_months: int, bands: dict):
    """Trouve la bande de couverture applicable."""
    pair_bands = bands.get(pair, [])
    for band in pair_bands:
        if band["min_months"] <= maturity_months < band["max_months"]:
            return band
    return pair_bands[-1] if pair_bands else None


def compute_position_in_band(signal_str: str, flow_type: str) -> float:
    """
    Position dans la bande : 0% = bas, 100% = haut.
    Importateur : achat de devise. Exportateur : vente de devise.
    """
    base = {
        "STRONG_BUY": 0.0,   # Devise forte → attendre (bas)
        "BUY": 0.25,
        "NEUTRAL": 0.50,
        "SELL": 0.75,
        "STRONG_SELL": 1.0,  # Devise faible → couvrir vite (haut)
    }.get(signal_str, 0.50)
    
    # Inverser pour exportateur (logique inverse)
    if flow_type == "exporter":
        base = 1.0 - base
    
    return base


def select_instrument(status: str, maturity_months: int) -> str:
    """Sélectionne l'instrument selon les règles métier."""
    if status == "firm" and maturity_months <= 12:
        return "Forward"
    elif status == "forecast" and maturity_months > 6:
        return "Option"
    elif maturity_months > 12:
        return "Swap"
    else:
        return "Forward"


def compute_forward_rate(spot: float, maturity_months: int, pair: str) -> float:
    """Approximation pédagogique du taux à terme."""
    premiums = {"EURUSD": 0.005, "EURTND": 0.015, "USDTND": 0.015}
    premium = premiums.get(pair, 0.01)
    forward = spot * (1 + premium * (maturity_months / 12))
    return round(forward, 4)


def process_client_request(amount: float, currency: str, maturity_months: int,
                           status: str, budget_rate: float, flow_type: str) -> dict:
    """
    Logique métier complète du module client.
    """
    bands, limits = load_policy()
    pair = f"{currency}TND" if currency in ["EUR", "USD"] else "EURUSD"
    
    # 1. Bande applicable
    band = get_band(pair, maturity_months, bands)
    if not band:
        return {"error": "Aucune bande définie pour cette échéance"}
    
    # 2. Ajustement ferme/prévision
    coverage_pct = band["coverage_pct"]
    if status == "forecast":
        coverage_pct *= 0.5
    
    # 3. Signal combiné (Couche 2)
    signal_data = combined_signal(pair)
    signal_str = signal_data["final_signal"]
    
    # 4. Positionnement précis dans la bande
    position = compute_position_in_band(signal_str, flow_type)
    band_range = band["band_upper"] - band["band_lower"]
    target_rate = band["band_lower"] + (band_range * position)
    
    # 5. Spot et forward
    spot = get_spot(pair)
    forward_rate = compute_forward_rate(spot, maturity_months, pair)
    
    # 6. Instrument
    instrument = select_instrument(status, maturity_months)
    
    # 7. Calculs financiers
    amount_to_cover = amount * coverage_pct
    cost = abs(forward_rate - spot) * amount_to_cover
    budget_gap = forward_rate - budget_rate
    
    # 8. Justification
    fund_reason = ""
    if signal_data["breakdown"]["fundamental"].get("reasons"):
        fund_reason = signal_data["breakdown"]["fundamental"]["reasons"][0]
    
    justification = (
        f"Signal {signal_str}. Position à {position*100:.0f}% dans la bande. "
        f"Contexte : {fund_reason if fund_reason else 'Macro neutre'}."
    )
    
    return {
        "montant_a_couvrir": round(amount_to_cover, 2),
        "pct_dans_bande": f"{position*100:.0f}%",
        "instrument": instrument,
        "taux_a_terme": forward_rate,
        "cout_couverture": round(cost, 2),
        "ecart_vs_budget": round(budget_gap, 4),
        "justification": justification,
        "meta": {
            "spot": spot,
            "bande": f"{band['band_lower']} - {band['band_upper']}",
            "coverage_pct": f"{coverage_pct*100:.0f}%",
            "signal_detail": signal_data
        }
    }


if __name__ == "__main__":
    import json as _json
    
    print("=" * 50)
    print("TEST 1 : Importateur EUR/TND, 500k, 3 mois, ferme")
    print("=" * 50)
    r1 = process_client_request(
        amount=500000,
        currency="EUR",
        maturity_months=3,
        status="firm",
        budget_rate=3.42,
        flow_type="importer"
    )
    print(_json.dumps(r1, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 50)
    print("TEST 2 : Exportateur EUR/TND, 300k, 6 mois, prévision")
    print("=" * 50)
    r2 = process_client_request(
        amount=300000,
        currency="EUR",
        maturity_months=6,
        status="forecast",
        budget_rate=3.40,
        flow_type="exporter"
    )
    print(_json.dumps(r2, indent=2, ensure_ascii=False))