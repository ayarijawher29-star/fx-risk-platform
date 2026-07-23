from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import MacroIndicator

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

indicators = session.query(MacroIndicator.indicator).distinct().all()
print(f"📊 Indicateurs présents : {[i[0] for i in indicators]}")
print(f"📊 Total lignes : {session.query(MacroIndicator).count()}")

print("\n📋 Derniers FED_RATE :")
rows = session.query(MacroIndicator).filter(MacroIndicator.indicator == "FED_RATE").order_by(MacroIndicator.date.desc()).limit(3).all()
for r in rows:
    print(f"  {r.date} | {r.value}")

session.close()