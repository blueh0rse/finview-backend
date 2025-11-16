from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from api.models.assets import Asset
from api.services.assets import get_all_assets


router = APIRouter(tags=["Assets"])


@router.get("/assets", response_model=List[Asset])
async def get_assets(skip: int = 0, limit: int = 10):
    """Retrieve all assets"""
    print("[REQ] GET /assets")
    assets = await get_all_assets(skip, limit)
    if not assets:
        raise HTTPException(status_code=204)
    return assets

