"""
Bloc Sentiment V1 — Approche allégée
Pas d'API LLM. Scoring par mots-clés + saisie manuelle possible.
"""

# Dictionnaire de mots-clés par banque centrale
KEYWORDS = {
    "restrictive": ["restrictif", "restrictive", "resserrement", "tightening", "hawkish", "lutte contre l'inflation", "vigilant"],
    "accommodative": ["accommodant", "accommodative", "assouplissement", "easing", "dovish", "soutien", "relance"],
    "neutral": ["neutre", "neutral", "patient", "data-dependent", "attentif", "prudent"]
}

def score_sentiment_text(text: str) -> dict:
    """
    Analyse simple d'un texte de communiqué.
    Retourne un score entre -1 (accommodant) et +1 (restrictif).
    """
    text_lower = text.lower()
    
    restrictive_count = sum(1 for word in KEYWORDS["restrictive"] if word in text_lower)
    accommodative_count = sum(1 for word in KEYWORDS["accommodative"] if word in text_lower)
    neutral_count = sum(1 for word in KEYWORDS["neutral"] if word in text_lower)
    
    total = restrictive_count + accommodative_count + neutral_count
    if total == 0:
        return {"score": 0, "label": "NEUTRAL", "reason": "Aucun mot-clé trouvé"}
    
    # Score pondéré
    raw_score = (restrictive_count - accommodative_count) / total
    
    if raw_score > 0.3:
        score, label = 1, "RESTRICTIVE"
    elif raw_score < -0.3:
        score, label = -1, "ACCOMMODATIVE"
    else:
        score, label = 0, "NEUTRAL"
    
    return {
        "score": score,
        "label": label,
        "reason": f"Restrictif: {restrictive_count}, Accommodant: {accommodative_count}, Neutre: {neutral_count}",
        "raw_score": round(raw_score, 3)
    }

def get_manual_sentiment(institution: str = "FED", score: float = 0.0) -> dict:
    """
    Pour la V1, le sentiment peut être saisi manuellement.
    institution: FED, BCE, ou BCT
    score: -1 (accommodant), 0 (neutre), +1 (restrictif)
    """
    labels = {1: "RESTRICTIVE", 0: "NEUTRAL", -1: "ACCOMMODATIVE"}
    return {
        "institution": institution,
        "score": score,
        "label": labels.get(score, "NEUTRAL"),
        "source": "manual_input"
    }

def get_default_sentiments() -> dict:
    """Point d'entrée V1 — sentiments par défaut (neutre)."""
    return {
        "FED": get_manual_sentiment("FED", 0),
        "BCE": get_manual_sentiment("BCE", 0),
        "BCT": get_manual_sentiment("BCT", 0)
    }

if __name__ == "__main__":
    # Test avec un texte Fed
    fed_text = "The Federal Reserve remains vigilant in its fight against inflation and may consider further tightening if data warrants."
    result = score_sentiment_text(fed_text)
    print(f"📊 SENTIMENT TEST")
    print(f"Texte : {fed_text[:60]}...")
    print(f"Score : {result['score']} ({result['label']})")
    print(f"Raison : {result['reason']}")
    
    # Test défaut
    defaults = get_default_sentiments()
    print(f"\n📊 SENTIMENTS PAR DÉFAUT :")
    for inst, data in defaults.items():
        print(f"  {inst}: {data['label']} (score: {data['score']})")