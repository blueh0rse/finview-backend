from fastapi import APIRouter
from api.services.portfolio import calc_portfolio_value, calc_portfolio_allocation

router = APIRouter(tags=["portfolio"])


@router.get("/portfolio/value")
async def get_portfolio_value():
    """Retrieve portfolio value"""
    print("[REQ] GET /portfolio/value")
    value = await calc_portfolio_value()
    return {"value": value}


@router.get("/portfolio/allocation")
async def get_portfolio_allocation():
    """Retrieve portfolio allocation"""
    print("[REQ] GET /portfolio/allocation")
    total_value, allocation = await calc_portfolio_allocation()
    return {"total_value": total_value, "allocation": allocation}
