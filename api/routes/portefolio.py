from fastapi import APIRouter
from api.services.portefolio import calc_portefolio_value, calc_portfolio_allocation

router = APIRouter(tags=["Portefolio"])


@router.get("/portefolio/value")
async def get_portfolio_value():
    """Retrieve portefolio value"""
    print("[REQ] GET /portefolio/value")
    value = await calc_portefolio_value()
    return {"value": value}


@router.get("/portefolio/allocation")
async def get_portfolio_allocation():
    """Retrieve portefolio allocation"""
    print("[REQ] GET /portefolio/allocation")
    total_value, allocation = await calc_portfolio_allocation()
    return {"total_value": total_value, "allocation": allocation}
