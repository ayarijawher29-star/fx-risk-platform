from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import MacroIndicator, FXFixingTND

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


def get_latest_macro(country: str, indicator: str):
    """Récupère la dernière valeur d'un indicateur macro."""
    session = SessionLocal()
    row = session.query(MacroIndicator).filter(
        MacroIndicator.country == country,
        MacroIndicator.indicator == indicator
    ).order_by(MacroIndicator.date.desc()).first()
    session.close()
    return row.value if row else None


def get_latest_tnd_fixing():
    """Récupère le dernier fixing TND."""
    session = SessionLocal()
    row = session.query(FXFixingTND).order_by(FXFixingTND.date.desc()).first()
    session.close()
    
    if row is None:
        return None, None
    
    return row.eur_tnd, row.usd_tnd


def score_fundamental_eurusd() -> dict:
    """Scoring EUR/USD basé sur les données macro US (FRED)."""
    fed_rate = get_latest_macro("US", "FED_RATE")
    cpi = get_latest_macro("US", "CPI")
    unemployment = get_latest_macro("US", "UNEMPLOYMENT")
    gdp = get_latest_macro("US", "GDP")
    
    score = 0
    reasons = []
    
    # Fed Rate
    if fed_rate is not None:
        if fed_rate >= 5.0:
            score += 1
            reasons.append(f"Fed rate élevé ({fed_rate}%) → USD fort")
        elif fed_rate <= 2.0:
            score -= 1
            reasons.append(f"Fed rate bas ({fed_rate}%) → USD faible")
        else:
            reasons.append(f"Fed rate neutre ({fed_rate}%)")
    
    # Inflation
    if cpi is not None:
        if cpi >= 300:
            score += 1
            reasons.append(f"Inflation US élevée ({cpi})")
        elif cpi <= 280:
            score -= 1
            reasons.append(f"Inflation US faible ({cpi})")
    
    # Chômage
    if unemployment is not None:
        if unemployment <= 4.0:
            score += 1
            reasons.append(f"Chômage faible ({unemployment}%) → économie solide")
        elif unemployment >= 6.0:
            score -= 1
            reasons.append(f"Chômage élevé ({unemployment}%)")
    
    # Signal final
    if score >= 2:
        signal = "STRONG_SELL"
    elif score == 1:
        signal = "SELL"
    elif score == -1:
        signal = "BUY"
    elif score <= -2:
        signal = "STRONG_BUY"
    else:
        signal = "NEUTRAL"
    
    return {
        "pair": "EURUSD",
        "score": score,
        "signal": signal,
        "reasons": reasons,
        "indicators": {
            "fed_rate": fed_rate,
            "cpi": cpi,
            "unemployment": unemployment,
            "gdp": gdp
        }
    }


def score_fundamental_tnd(pair: str = "EURTND") -> dict:
    """Scoring pour EUR/TND et USD/TND."""
    eur_tnd, usd_tnd = get_latest_tnd_fixing()
    
    score = 0
    reasons = []
    
    if eur_tnd is not None:
        if eur_tnd >= 3.45:
            score -= 1
            reasons.append(f"EUR/TND élevé ({eur_tnd}) → risque correction BCT")
        elif eur_tnd <= 3.30:
            score += 1
            reasons.append(f"EUR/TND bas ({eur_tnd}) → potentiel hausse")
        else:
            reasons.append(f"EUR/TND stable ({eur_tnd})")
    else:
        reasons.append("Pas de données TND disponibles")
    
    if score >= 1:
        signal = "BUY"
    elif score <= -1:
        signal = "SELL"
    else:
        signal = "NEUTRAL"
    
    return {
        "pair": pair,
        "score": score,
        "signal": signal,
        "reasons": reasons,
        "fixing": {"eur_tnd": eur_tnd, "usd_tnd": usd_tnd}
    }


def get_fundamental_signals() -> dict:
    """Point d'entrée principal."""
    return {
        "EURUSD": score_fundamental_eurusd(),
        "EURTND": score_fundamental_tnd("EURTND"),
        "USDTND": score_fundamental_tnd("USDTND")
    }


if __name__ == "__main__":
    results = get_fundamental_signals()
    for pair, data in results.items():
        print(f"\n📊 FONDAMENTAL {pair}")
        print(f"Signal : {data['signal']} | Score : {data['score']}")
        print(f"Raisons : {data['reasons']}")