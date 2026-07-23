import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import MacroIndicator


FRED_API_KEY = "0ed09e9c70e409c517c63a74f6a6835c"

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

SERIES = {
    "FEDFUNDS": {"country": "US", "indicator": "FED_RATE", "freq": "monthly"},
    "CPIAUCSL": {"country": "US", "indicator": "CPI", "freq": "monthly"},
    "PAYEMS":   {"country": "US", "indicator": "NFP", "freq": "monthly"},
    "GDP":      {"country": "US", "indicator": "GDP", "freq": "quarterly"},
    "UNRATE":   {"country": "US", "indicator": "UNEMPLOYMENT", "freq": "monthly"},
}

start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
print(f"📥 Récupération FRED depuis {start_date}...")

total_inserted = 0

for series_id, meta in SERIES.items():
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        observations = data.get("observations", [])
        print(f"  📊 {series_id} ({meta['indicator']}): {len(observations)} observations")
        
        for obs in observations:
            val = obs.get("value")
            if val and val != ".":
                date_obj = datetime.strptime(obs["date"], "%Y-%m-%d").date()
                session.query(MacroIndicator).filter(
                    MacroIndicator.date == date_obj,
                    MacroIndicator.country == meta["country"],
                    MacroIndicator.indicator == meta["indicator"]
                ).delete()
                
                entry = MacroIndicator(
                    date=date_obj,
                    country=meta["country"],
                    indicator=meta["indicator"],
                    value=float(val),
                    frequency=meta["freq"]
                )
                session.add(entry)
                total_inserted += 1
        
        session.commit()
    except Exception as e:
        print(f"  ❌ Erreur {series_id}: {e}")

session.close()
print(f"\n✅ Total inséré : {total_inserted} lignes")