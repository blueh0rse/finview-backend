from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from api.models.assets import Asset, AssetCreate, AssetUpdate
from api.services.assets import (
    create_one_asset,
    delete_one_asset,
    get_all_assets,
    get_asset_by_symbol,
    update_one_asset,
)


router = APIRouter(tags=["Assets"])


@router.get("/assets", response_model=List[Asset])
async def get_assets(skip: int = 0, limit: int = 10):
    """Retrieve all assets"""
    print("[REQ] GET /assets")
    assets = await get_all_assets(skip, limit)
    if not assets:
        raise HTTPException(status_code=204)
    return assets


@router.get("/assets/{symbol}", response_model=Asset)
async def get_asset(symbol: str):
    """Retrieve a specific asset by symbol"""
    print(f"[REQ] GET /assets/{symbol}")
    asset = await get_asset_by_symbol(symbol)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/assets", response_model=Asset, status_code=201)
async def create_asset(asset: AssetCreate):
    """Create a new asset"""
    print(f"[REQ] POST /assets {asset.symbol} - {asset.category}")
    try:
        created_asset = await create_one_asset(asset)
        if created_asset is None:
            raise HTTPException(status_code=400, detail="Failed to create asset")
        return created_asset
    except ValueError as e:
        # asset symbol already exists
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/assets/{symbol}", response_model=Asset)
async def update_asset(symbol: str, asset: AssetUpdate):
    """Update an existing asset by symbol"""
    print(f"[REQ] PUT /assets/{symbol}")
    try:
        return await update_one_asset(symbol, asset)
    except ValueError:
        raise HTTPException(404, "Asset not found")


@router.delete("/assets/{symbol}", status_code=204)
async def delete_asset(symbol: str):
    """Delete a specific asset by symbol"""
    print(f"[REQ] DELETE /assets/{symbol}")
    deleted = await delete_one_asset(symbol)
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    return deleted
