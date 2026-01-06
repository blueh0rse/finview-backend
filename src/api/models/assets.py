import re
from datetime import datetime, timezone
from pydantic import BaseModel, StrictStr, StrictFloat, field_validator

# 2–10 uppercase letters, no spaces or special characters (e.g. BTC, ETH)
ASSET_SYMBOL_REGEX = re.compile(r"^[A-Z]{2,10}$")

# 2–50 characters, alphanumeric plus basic punctuation (.,'- and spaces)
ASSET_NAME_REGEX = re.compile(r"^[A-Za-z0-9 .,'-]{2,50}$")

# 3–30 characters, alphanumeric and underscores (e.g. Stock, CRYPTO)
ASSET_CATEGORY_REGEX = re.compile(r"^[A-ZA-Za-z_]{3,30}$")


class AssetValidators:
    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str | None) -> str | None:
        if v is not None and not ASSET_SYMBOL_REGEX.fullmatch(v):
            raise ValueError("symbol must be 2-10 uppercase letters")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None and not ASSET_NAME_REGEX.fullmatch(v):
            raise ValueError("invalid asset name format")
        return v.strip() if v else v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str | None) -> str | None:
        if v is not None and not ASSET_CATEGORY_REGEX.fullmatch(v):
            raise ValueError("category must be uppercase snake case")
        return v

    @field_validator("current_price")
    @classmethod
    def validate_price(cls, v: float | None) -> float | None:
        if v is not None and v <= 0:
            raise ValueError("current_price must be > 0")
        return v

    @field_validator("updated_at")
    @classmethod
    def validate_updated_at(cls, v: datetime | None) -> datetime | None:
        if v is None:
            return v
        # Normalize naive datetimes to UTC and convert aware datetimes to UTC
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        else:
            v = v.astimezone(timezone.utc)
        if v > datetime.now(tz=timezone.utc):
            raise ValueError("updated_at cannot be in the future")
        return v


class AssetBase(BaseModel, AssetValidators):
    symbol: StrictStr
    name: StrictStr
    category: StrictStr
    current_price: StrictFloat | None = None
    updated_at: datetime | None = None


class Asset(AssetBase):
    class Config:
        from_attributes = True


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel, AssetValidators):
    symbol: StrictStr | None = None
    name: StrictStr | None = None
    category: StrictStr | None = None
    current_price: StrictFloat | None = None
    updated_at: datetime | None = None
