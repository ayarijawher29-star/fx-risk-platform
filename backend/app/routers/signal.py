from fastapi import APIRouter
from app.engine.combiner import combined_signal

router = APIRouter(prefix="/signal", tags=["signal"])

@router.get("/{pair}")
def get_signal(pair: str):
    valid_pairs = ["EURUSD", "EURTND", "USDTND"]
    if pair.upper() not in valid_pairs:
        return {"error": f"Invalid pair. Use one of {valid_pairs}"}
    return combined_signal(pair.upper())