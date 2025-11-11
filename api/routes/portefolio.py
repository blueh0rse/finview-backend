from fastapi import APIRouter
from api.services.portefolio import get_portefolio_value

router = APIRouter(tags=["Transactions"])


@router.get("/portefolio/value")
async def get_transactions():
    """Retrieve portefolio value"""
    print("[REQ] GET /portefolio/value")
    value = await get_portefolio_value()
    return {"value": value}
