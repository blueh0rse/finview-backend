from typing import List
import uuid

from api.db.db import SessionLocal
from api.models.assets import Asset, AssetCreate
from api.schemas.assets import AssetORM


MAX_ASSETS = 100


async def get_all_assets(skip, limit) -> List[Asset]:
    print("[ASSET] GET ALL")
    if limit > MAX_ASSETS:
        limit = MAX_ASSETS

    db = SessionLocal()
    try:
        assets = db.query(AssetORM).offset(skip).limit(limit).all()
        return [Asset.model_validate(tx) for tx in assets]
    finally:
        db.close()


async def get_asset_by_id(asset_id: uuid.UUID) -> Asset:
    print(f"[ASSET] GET BY ID {asset_id}")
    db = SessionLocal()
    try:
        tx = db.query(AssetORM).filter(AssetORM.id == asset_id).first()
        if not tx:
            return False
        return Asset.model_validate(tx)
    finally:
        db.close()


async def create_one_asset(asset: AssetCreate) -> Asset:
    print(f"[ASSET] CREATE {asset.symbol} - {asset.category}")
    # ensure asset symbol is uppercase
    asset.symbol = asset.symbol.upper()

    db = SessionLocal()
    try:
        tx = AssetORM(**asset.model_dump())
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return Asset.model_validate(tx)
    except Exception as e:
        db.rollback()
        print("[ERROR] create_asset:", e)
        raise
    finally:
        db.close()
