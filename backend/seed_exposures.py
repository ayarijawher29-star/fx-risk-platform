from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import ClientExposure

engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Deal 1 : Importateur tunisien achète 500k EUR (3 mois, ferme)
exp1 = ClientExposure(
    amount=500000,
    currency="EUR",
    maturity_months=3,
    status="firm",
    budget_rate=3.42,
    flow_type="importer"
)

# Deal 2 : Exportateur tunisien vend 300k EUR (6 mois, prévision)
exp2 = ClientExposure(
    amount=300000,
    currency="EUR",
    maturity_months=6,
    status="forecast",
    budget_rate=3.40,
    flow_type="exporter"
)

# Deal 3 : Importateur achète 200k USD (3 mois, ferme)
exp3 = ClientExposure(
    amount=200000,
    currency="USD",
    maturity_months=3,
    status="firm",
    budget_rate=3.18,
    flow_type="importer"
)

session.add_all([exp1, exp2, exp3])
session.commit()
session.close()

print("✅ 3 deals clients injectés dans la base.")