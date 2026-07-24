from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.client_module import process_client_request

router = APIRouter(prefix="/client", tags=["client"])

class ClientRequest(BaseModel):
    amount: float
    currency: str
    maturity_months: int
    status: str  # "firm" or "forecast"
    budget_rate: float
    flow_type: str  # "importer" or "exporter"

@router.post("/analyze")
def analyze_client(req: ClientRequest):
    return process_client_request(
        amount=req.amount,
        currency=req.currency,
        maturity_months=req.maturity_months,
        status=req.status,
        budget_rate=req.budget_rate,
        flow_type=req.flow_type
    )