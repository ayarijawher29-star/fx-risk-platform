from app.data.models import Base
from sqlalchemy import create_engine

# Crée le fichier fx_data.db à côté de ce script
engine = create_engine("sqlite:///fx_data.db", echo=True)

# Crée toutes les tables
Base.metadata.create_all(bind=engine)

print("✅ Base de données fx_data.db créée avec succès.")
print("Tables créées : market_data, fx_fixing_tnd, macro_indicators, client_exposures, coverage_bands, trader_positions")