import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from app.data.models import FXFixingTND

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

today = datetime.now().date()
print(f"📅 Date du jour : {today}")

# Essayer le scraping BCT
try:
    print("🌐 Tentative de scraping BCT...")
    url = "https://www.bct.gov.tn/bct/siteprod/cours.jsp"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    
    eur_val = None
    usd_val = None
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                text = cells[0].get_text(strip=True).upper()
                if "EUR" in text:
                    eur_val = float(cells[1].get_text(strip=True).replace(",", "."))
                elif "USD" in text:
                    usd_val = float(cells[1].get_text(strip=True).replace(",", "."))
    
    if eur_val and usd_val:
        session.query(FXFixingTND).filter(FXFixingTND.date == today).delete()
        session.commit()
        
        entry = FXFixingTND(date=today, eur_tnd=eur_val, usd_tnd=usd_val, source="scraping")
        session.add(entry)
        session.commit()
        print(f"✅ Scraping réussi : EUR/TND = {eur_val}, USD/TND = {usd_val}")
    else:
        raise ValueError("Cours non trouvés dans le HTML")

except Exception as e:
    print(f"⚠️ Scraping échoué : {e}")
    print("📂 Utilisation du fallback...")
    
    with open("../data/static/tnd_fallback.json", "r") as f:
        fallback = json.load(f)
    
    session.query(FXFixingTND).filter(FXFixingTND.date == today).delete()
    session.commit()
    
    entry = FXFixingTND(
        date=today,
        eur_tnd=fallback["eur_tnd"],
        usd_tnd=fallback["usd_tnd"],
        source="manual"
    )
    session.add(entry)
    session.commit()
    print(f"✅ Fallback inséré : EUR/TND = {fallback['eur_tnd']}, USD/TND = {fallback['usd_tnd']}")

session.close()