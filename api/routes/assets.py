from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from api.models.assets import Asset, AssetCreate
from api.services.assets import create_one_asset, get_all_assets


router = APIRouter(tags=["Assets"])


@router.get("/assets", response_model=List[Asset])
async def get_assets(skip: int = 0, limit: int = 10):
    """Retrieve all assets"""
    print("[REQ] GET /assets")
    assets = await get_all_assets(skip, limit)
    if not assets:
        raise HTTPException(status_code=204)
    return assets


@router.post("/assets", response_model=Asset, status_code=201)
async def create_asset(asset: AssetCreate):
    """Create a new asset"""
    print(f"[REQ] POST /assets {asset.symbol} - {asset.category}")
    created_asset = await create_one_asset(asset)
    if created_asset is None:
        raise HTTPException(status_code=400, detail="Failed to create asset")
    return created_asset
