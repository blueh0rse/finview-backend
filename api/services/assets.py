from typing import List

from api.db.db import SessionLocal
from api.models.assets import AssetRead
from api.schemas.assets import AssetORM


MAX_ASSETS = 100

    
async def get_all_assets(skip, limit) -> List[AssetRead]:
    print("[ASSET] GET ALL")
    if limit > MAX_ASSETS:
        limit = MAX_ASSETS
    db = SessionLocal()
    try:
        assets = db.query(AssetORM).offset(skip).limit(limit).all()
        return [AssetRead.model_validate(tx) for tx in assets]
    finally:
        db.close()
