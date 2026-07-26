from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import market, signal, client, trader
from app.data.seed_on_startup import seed_database

# Recharger les données au démarrage (critique pour Render)
seed_database()

app = FastAPI(
    title="FX Risk Management Platform",
    description="Plateforme d'aide à la décision de couverture FX",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router)
app.include_router(signal.router)
app.include_router(client.router)
app.include_router(trader.router)

@app.get("/")
def root():
    return {"message": "FX Risk Platform API", "status": "running"}