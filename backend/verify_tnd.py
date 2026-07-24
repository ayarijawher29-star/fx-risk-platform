from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import FXFixingTND

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

rows = session.query(FXFixingTND).all()
for r in rows:
    print(f"{r.date} | EUR/TND: {r.eur_tnd} | USD/TND: {r.usd_tnd} | Source: {r.source}")

session.close()