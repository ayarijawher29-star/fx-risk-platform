from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import MarketData

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Compter les lignes
count = session.query(MarketData).filter(MarketData.pair == "EURUSD").count()
print(f"📊 Nombre total de lignes EUR/USD : {count}")

# Afficher les 5 premières lignes
print("\n📋 5 premières lignes :")
rows = session.query(MarketData).filter(MarketData.pair == "EURUSD").order_by(MarketData.date).limit(5).all()
for r in rows:
    print(f"  {r.date} | Open: {r.open:.4f} | High: {r.high:.4f} | Low: {r.low:.4f} | Close: {r.close:.4f}")

# Afficher les 5 dernières lignes
print("\n📋 5 dernières lignes :")
rows = session.query(MarketData).filter(MarketData.pair == "EURUSD").order_by(MarketData.date.desc()).limit(5).all()
for r in rows:
    print(f"  {r.date} | Open: {r.open:.4f} | High: {r.high:.4f} | Low: {r.low:.4f} | Close: {r.close:.4f}")

session.close()
print("\n✅ La base contient bien des données.")