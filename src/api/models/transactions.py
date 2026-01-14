import re
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, StrictStr, StrictFloat, field_validator

# 2–10 uppercase letters, no spaces or special characters
TRANSACTION_ASSET_SYMBOL_REGEX = re.compile(r"^[A-Z]{2,10}$")

# ISO 4217 uppercase (3 letters)
TRANSACTION_CURRENCY_REGEX = re.compile(r"^[A-Z]{3}$")

# up to 255 chars, readable text, no control characters
TRANSACTION_COMMENT_REGEX = re.compile(r"^[A-Za-z0-9 .,'\"!?()\-]{0,255}$")


class TransactionValidators:
    @field_validator("asset_symbol")
    @classmethod
    def validate_asset_symbol(cls, v: str | None) -> str | None:
        if v is not None and not TRANSACTION_ASSET_SYMBOL_REGEX.fullmatch(v):
            raise ValueError("asset_symbol must be 2-10 uppercase letters")
        return v

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str | None) -> str | None:
        if v is not None and not TRANSACTION_CURRENCY_REGEX.fullmatch(v):
            raise ValueError("currency must be 3 uppercase letters (ISO 4217)")
        return v

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, v: str | None) -> str | None:
        if v is not None and not TRANSACTION_COMMENT_REGEX.fullmatch(v):
            raise ValueError("comment contains invalid characters or is too long")
        return v.strip() if v else v

    @field_validator("amount", "quantity", "unit_price")
    @classmethod
    def validate_positive_float(cls, v: float | None) -> float | None:
        if v is not None and v <= 0:
            raise ValueError("must be a positive number")
        return v

    @field_validator("date")
    @classmethod
    def validate_date_not_future(cls, v: datetime | None) -> datetime | None:
        if v is None:
            return v
        # Normalize naive datetimes to UTC and convert aware datetimes to UTC
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        else:
            v = v.astimezone(timezone.utc)
        if v > datetime.now(tz=timezone.utc):
            raise ValueError("date cannot be in the future")
        return v


class TransactionBase(BaseModel, TransactionValidators):
    asset_symbol: StrictStr
    operation: Literal["buy", "sell"]
    amount: StrictFloat
    quantity: StrictFloat
    unit_price: StrictFloat
    currency: StrictStr
    date: datetime
    comment: StrictStr | None = None


class Transaction(TransactionBase):
    id: UUID

    class ConfigDict:
        from_attributes = True


class TransactionCreate(TransactionBase):
    class ConfigDict:
        from_attributes = True


class TransactionUpdate(BaseModel, TransactionValidators):
    asset_symbol: StrictStr | None = None
    operation: Literal["buy", "sell"] | None = None
    amount: StrictFloat | None = None
    quantity: StrictFloat | None = None
    unit_price: StrictFloat | None = None
    currency: StrictStr | None = None
    date: datetime | None = None
    comment: StrictStr | None = None

    class ConfigDict:
        from_attributes = True
