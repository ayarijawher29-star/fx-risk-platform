from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import market, signal, client, trader

app = FastAPI(
    title="FX Risk Management Platform",
    description="Plateforme d'aide à la décision de couverture FX",
    version="1.0.0"
)

# CORS pour le frontend React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(market.router)
app.include_router(signal.router)
app.include_router(client.router)
app.include_router(trader.router)

@app.get("/")
def root():
    return {"message": "FX Risk Platform API", "status": "running"}