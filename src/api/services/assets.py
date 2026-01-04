from typing import List

from psycopg2 import IntegrityError

from src.api.db.db import SessionLocal
from src.api.models.assets import Asset, AssetCreate, AssetUpdate
from src.api.schemas.assets import AssetORM


MAX_ASSETS = 100


class AssetNotFoundError(Exception):
    pass


class AssetConflictError(Exception):
    pass


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


async def get_asset_by_symbol(symbol: str) -> Asset:
    print(f"[ASSET] GET BY SYMBOL {symbol}")
    db = SessionLocal()
    try:
        tx = db.query(AssetORM).filter(AssetORM.symbol == symbol.upper()).first()
        if not tx:
            return False
        return Asset.model_validate(tx)
    finally:
        db.close()


async def create_one_asset(asset: AssetCreate) -> Asset:
    print(f"[ASSET] CREATE {asset.symbol} - {asset.category}")
    # ensure asset symbol is uppercase
    asset.symbol = asset.symbol.upper()

    # ensure asset symbol is unique
    existing_asset = await get_asset_by_symbol(asset.symbol)
    if existing_asset:
        raise ValueError(f"Asset {asset.symbol} already exists")

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


async def update_one_asset(current_symbol: str, asset: AssetUpdate) -> Asset:
    print(f"[ASSET] UPDATE {current_symbol.upper()}")
    db = SessionLocal()
    try:
        symbol = current_symbol.upper()

        existing_asset = db.query(AssetORM).filter(AssetORM.symbol == symbol).first()
        if not existing_asset:
            raise AssetNotFoundError(f"Asset '{symbol}' not found")

        # ensure asset symbol is uppercase
        if asset.symbol:
            asset.symbol = asset.symbol.upper()

        # only provided fields will be updated
        updates = asset.model_dump(exclude_unset=True)

        # apply updates
        for field, value in updates.items():
            setattr(existing_asset, field, value)

        db.commit()
        db.refresh(existing_asset)

        return Asset.model_validate(existing_asset)

    except IntegrityError:
        db.rollback()
        raise AssetConflictError("Asset with this unique field already exists")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


async def delete_one_asset(symbol: str) -> bool:
    print(f"[ASSET] DELETE {symbol}")
    db = SessionLocal()
    try:
        tx = db.query(AssetORM).filter(AssetORM.symbol == symbol.upper()).first()
        if not tx:
            return False
        db.delete(tx)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print("[ERROR] delete_asset:", e)
        raise
    finally:
        db.close()
