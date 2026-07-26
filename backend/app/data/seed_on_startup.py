"""
Script exécuté au démarrage du serveur pour recharger les données.
Garantit que SQLite n'est jamais vide, même après un redémarrage Render.
"""

import os
import sys

# Ajouter le dossier backend au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import Base, MarketData, FXFixingTND, MacroIndicator
from datetime import datetime, timedelta

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def seed_database():
    """Vérifie si la base a des données. Si non, recharge tout."""
    session = SessionLocal()
    
    # Vérifier s'il y a déjà des données
    market_count = session.query(MarketData).count()
    tnd_count = session.query(FXFixingTND).count()
    macro_count = session.query(MacroIndicator).count()
    
    session.close()
    
    print(f"📊 DB Check — Market: {market_count}, TND: {tnd_count}, Macro: {macro_count}")
    
    if market_count > 0 and tnd_count > 0 and macro_count > 0:
        print("✅ Base déjà peuplée. Skip.")
        return
    
    print("🔄 Rechargement des données...")
    
    # 1. EUR/USD via yfinance
    try:
        import yfinance as yf
        ticker = yf.Ticker("EURUSD=X")
        df = ticker.history(period="2y", interval="1d").reset_index()
        df.columns = [c.lower() for c in df.columns]
        df = df[["date", "open", "high", "low", "close", "volume"]]
        df["date"] = df["date"].dt.date
        df["pair"] = "EURUSD"
        df = df.dropna(subset=["close"])
        
        session = SessionLocal()
        session.query(MarketData).filter(MarketData.pair == "EURUSD").delete()
        for _, row in df.iterrows():
            session.add(MarketData(**row.to_dict()))
        session.commit()
        session.close()
        print(f"✅ EUR/USD : {len(df)} lignes")
    except Exception as e:
        print(f"⚠️ EUR/USD échec : {e}")
    
    # 2. TND fallback
    try:
        import json
        with open("../data/static/tnd_fallback.json", "r") as f:
            fallback = json.load(f)
        
        session = SessionLocal()
        today = datetime.now().date()
        session.query(FXFixingTND).filter(FXFixingTND.date == today).delete()
        session.add(FXFixingTND(
            date=today,
            eur_tnd=fallback["eur_tnd"],
            usd_tnd=fallback["usd_tnd"],
            source="manual"
        ))
        session.commit()
        session.close()
        print("✅ TND fallback inséré")
    except Exception as e:
        print(f"⚠️ TND échec : {e}")
    
    # 3. Macro FRED (si clé API disponible)
    try:
        import requests
        FRED_API_KEY = os.getenv("FRED_API_KEY", "")
        if not FRED_API_KEY:
            print("⚠️ Pas de clé FRED. Macro non chargée.")
            return
            
        SERIES = {
            "FEDFUNDS": {"country": "US", "indicator": "FED_RATE", "freq": "monthly"},
            "CPIAUCSL": {"country": "US", "indicator": "CPI", "freq": "monthly"},
            "PAYEMS": {"country": "US", "indicator": "NFP", "freq": "monthly"},
            "GDP": {"country": "US", "indicator": "GDP", "freq": "quarterly"},
            "UNRATE": {"country": "US", "indicator": "UNEMPLOYMENT", "freq": "monthly"},
        }
        
        start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
        session = SessionLocal()
        
        for series_id, meta in SERIES.items():
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                "series_id": series_id,
                "api_key": FRED_API_KEY,
                "file_type": "json",
                "observation_start": start_date,
            }
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            observations = data.get("observations", [])
            
            for obs in observations:
                val = obs.get("value")
                if val and val != ".":
                    date_obj = datetime.strptime(obs["date"], "%Y-%m-%d").date()
                    session.query(MacroIndicator).filter(
                        MacroIndicator.date == date_obj,
                        MacroIndicator.country == meta["country"],
                        MacroIndicator.indicator == meta["indicator"]
                    ).delete()
                    session.add(MacroIndicator(
                        date=date_obj,
                        country=meta["country"],
                        indicator=meta["indicator"],
                        value=float(val),
                        frequency=meta["freq"]
                    ))
            session.commit()
        
        session.close()
        print("✅ Macro FRED chargée")
    except Exception as e:
        print(f"⚠️ Macro échec : {e}")
    
    print("🎯 Seed terminé.")

if __name__ == "__main__":
    seed_database()