from fastapi import APIRouter
from app.modules.trader_module import process_trader_book

router = APIRouter(prefix="/trader", tags=["trader"])

@router.get("/book")
def get_trader_book():
    return process_trader_book()