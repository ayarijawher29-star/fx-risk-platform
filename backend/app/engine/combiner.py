from app.engine.technical import get_latest_technical_signal
from app.engine.fundamental import get_fundamental_signals
from app.engine.sentiment import get_default_sentiments

# Poids du CDC
WEIGHTS = {
    "EURUSD": {"technical": 0.50, "fundamental": 0.50},
    "EURTND": {"technical": 0.20, "fundamental": 0.80},
    "USDTND": {"technical": 0.20, "fundamental": 0.80},
}

SIGNAL_MAP = {
    "STRONG_BUY": 2,
    "BUY": 1,
    "NEUTRAL": 0,
    "SELL": -1,
    "STRONG_SELL": -2,
    "INSUFFICIENT_DATA": 0,
}

REVERSE_MAP = {
    2: "STRONG_BUY",
    1: "BUY",
    0: "NEUTRAL",
    -1: "SELL",
    -2: "STRONG_SELL",
}

def normalize_signal(signal_str: str) -> int:
    return SIGNAL_MAP.get(signal_str, 0)

def combined_signal(pair: str) -> dict:
    """
    Combine technique + fondamental + sentiment selon les poids CDC.
    """
    weights = WEIGHTS.get(pair, {"technical": 0.50, "fundamental": 0.50})
    
    # Récupérer les signaux
    tech = get_latest_technical_signal() if pair == "EURUSD" else {"score": 0, "signal": "NEUTRAL"}
    fund = get_fundamental_signals().get(pair, {"score": 0, "signal": "NEUTRAL"})
    sent = get_default_sentiments()  # V1 : neutre par défaut
    
    # Scores numériques
    tech_score = normalize_signal(tech["signal"])
    fund_score = fund["score"]
    
    # Sentiment V1 : ajustement léger (on prend FED pour EUR/USD, BCT pour TND)
    if pair == "EURUSD":
        sent_score = sent["FED"]["score"]
    else:
        sent_score = sent["BCT"]["score"]
    
    # Combinaison pondérée
    # Le sentiment V1 est intégré comme un ajustement léger du fondamental
    adjusted_fund = fund_score + (sent_score * 0.2)  # Sentiment pèse 20% du fondamental
    
    final_score = (tech_score * weights["technical"]) + (adjusted_fund * weights["fundamental"])
    
    # Arrondir et mapper
    rounded = round(final_score)
    if rounded > 2:
        rounded = 2
    if rounded < -2:
        rounded = -2
    
    final_signal = REVERSE_MAP.get(rounded, "NEUTRAL")
    
    return {
        "pair": pair,
        "final_signal": final_signal,
        "final_score": round(final_score, 2),
        "breakdown": {
            "technical": {"signal": tech["signal"], "score": tech_score, "weight": weights["technical"]},
            "fundamental": {"signal": fund["signal"], "score": fund_score, "weight": weights["fundamental"]},
            "sentiment": {"label": sent["FED"]["label"] if pair == "EURUSD" else sent["BCT"]["label"], "score": sent_score}
        },
        "details": tech.get("details", {}) if pair == "EURUSD" else {}
    }

def get_all_combined_signals() -> dict:
    """Point d'entrée principal."""
    return {
        "EURUSD": combined_signal("EURUSD"),
        "EURTND": combined_signal("EURTND"),
        "USDTND": combined_signal("USDTND")
    }

if __name__ == "__main__":
    results = get_all_combined_signals()
    for pair, data in results.items():
        print(f"\n🎯 COMBINÉ {pair}")
        print(f"Signal final : {data['final_signal']} (score: {data['final_score']})")
        print(f"Détail : Tech={data['breakdown']['technical']['signal']} | Fund={data['breakdown']['fundamental']['signal']}")