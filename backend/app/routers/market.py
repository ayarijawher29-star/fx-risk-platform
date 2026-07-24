from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data.models import MarketData, FXFixingTND, MacroIndicator

router = APIRouter(prefix="/market", tags=["market"])
engine = create_engine("sqlite:///fx_data.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

@router.get("/eurusd")
def get_eurusd_history(limit: int = 90):
    session = SessionLocal()
    rows = session.query(MarketData).filter(MarketData.pair == "EURUSD").order_by(MarketData.date.desc()).limit(limit).all()
    session.close()
    return {
        "pair": "EURUSD",
        "count": len(rows),
        "data": [{"date": str(r.date), "open": r.open, "high": r.high, "low": r.low, "close": r.close} for r in reversed(rows)]
    }

@router.get("/tnd")
def get_tnd_fixing():
    session = SessionLocal()
    row = session.query(FXFixingTND).order_by(FXFixingTND.date.desc()).first()
    session.close()
    if not row:
        return {"error": "No TND data"}
    return {"date": str(row.date), "eur_tnd": row.eur_tnd, "usd_tnd": row.usd_tnd, "source": row.source}

@router.get("/macro")
def get_macro_summary():
    session = SessionLocal()
    indicators = session.query(MacroIndicator).order_by(MacroIndicator.date.desc()).limit(20).all()
    session.close()
    return {
        "indicators": [
            {"date": str(i.date), "country": i.country, "indicator": i.indicator, "value": i.value}
            for i in indicators
        ]
    }