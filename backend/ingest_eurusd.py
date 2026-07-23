import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import MarketData, Base

# Connexion à la base
engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

print("📥 Téléchargement de l'historique EUR/USD (2 ans)...")

# Télécharger les données daily sur 2 ans
ticker = yf.Ticker("EURUSD=X")
df = ticker.history(period="2y", interval="1d")

print(f"✅ {len(df)} lignes téléchargées")

# Nettoyer les données
df = df.reset_index()
df = df.rename(columns={
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
})

# yfinance retourne parfois des colonnes avec majuscules, parfois non
# On s'assure que tout est en minuscule
df.columns = [c.lower() for c in df.columns]

# Garder uniquement les colonnes utiles
df = df[["date", "open", "high", "low", "close", "volume"]]
df["pair"] = "EURUSD"

# Supprimer les lignes où close est NaN (week-ends, jours fériés)
df = df.dropna(subset=["close"])

# Convertir la date en format date (sans l'heure)
df["date"] = pd.to_datetime(df["date"]).dt.date

# Supprimer les anciennes données EUR/USD si elles existent (pour éviter les doublons)
session.query(MarketData).filter(MarketData.pair == "EURUSD").delete()
session.commit()

# Insérer en bulk
records = df.to_dict(orient="records")
for record in records:
    entry = MarketData(**record)
    session.add(entry)

session.commit()
session.close()

print(f"✅ {len(records)} lignes insérées dans la table market_data")
print("Vérification : SELECT * FROM market_data WHERE pair = 'EURUSD'")