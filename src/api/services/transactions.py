from typing import List
import uuid
from sqlalchemy.exc import IntegrityError
from src.api.db.db import SessionLocal
from src.api.models.transactions import Transaction, TransactionCreate
from src.api.schemas.transactions import TransactionORM
from src.api.schemas.assets import AssetORM

MAX_TRANSACTIONS = 100


async def get_all_transactions(skip, limit) -> List[Transaction]:
    print("[TRANSACTION] GET ALL")
    if limit > MAX_TRANSACTIONS:
        limit = MAX_TRANSACTIONS
    db = SessionLocal()
    try:
        transactions = db.query(TransactionORM).offset(skip).limit(limit).all()
        return [Transaction.model_validate(tx) for tx in transactions]
    finally:
        db.close()


async def get_transaction_by_id(transaction_id: uuid.UUID) -> Transaction:
    print(f"[TRANSACTION] GET BY ID {transaction_id}")
    db = SessionLocal()
    try:
        tx = (
            db.query(TransactionORM).filter(TransactionORM.id == transaction_id).first()
        )
        if not tx:
            return False
        data = {k: v for k, v in tx.__dict__.items() if not k.startswith("_")}
        return Transaction(**data)
    finally:
        db.close()


async def create_one_transaction(transaction: TransactionCreate) -> Transaction:
    print(
        f"[TRANSACTION] CREATE {transaction.asset_symbol} - {transaction.operation} - {transaction.amount}{transaction.currency}"
    )
    # Check if asset exists
    db = SessionLocal()
    try:
        asset = (
            db.query(AssetORM)
            .filter(AssetORM.symbol == transaction.asset_symbol.upper())
            .first()
        )
        if not asset:
            raise ValueError(f"Asset {transaction.asset_symbol} does not exist")

        tx = TransactionORM(**transaction.model_dump())
        db.add(tx)
        db.commit()
        db.refresh(tx)
        data = {k: v for k, v in tx.__dict__.items() if not k.startswith("_")}
        return Transaction(**data)
    except IntegrityError:
        db.rollback()
        raise ValueError("Transaction creation failed due to constraint violation")
    except Exception as e:
        db.rollback()
        print("[ERROR] create_transaction:", e)
        raise
    finally:
        db.close()


async def update_one_transaction(transaction: Transaction) -> Transaction:
    print(f"[TRANSACTION] UPDATE {transaction.id}")
    db = SessionLocal()
    try:
        tx = (
            db.query(TransactionORM).filter(TransactionORM.id == transaction.id).first()
        )
        if not tx:
            return False
        for key, value in transaction.model_dump().items():
            setattr(tx, key, value)
        db.commit()
        db.refresh(tx)
        data = {k: v for k, v in tx.__dict__.items() if not k.startswith("_")}
        return Transaction(**data)
    except Exception as e:
        db.rollback()
        print("[ERROR] update_transaction:", e)
        raise
    finally:
        db.close()


async def delete_one_transaction(transaction_id: uuid.UUID) -> bool:
    print(f"[TRANSACTION] DELETE {transaction_id}")
    db = SessionLocal()
    try:
        tx = (
            db.query(TransactionORM).filter(TransactionORM.id == transaction_id).first()
        )
        if not tx:
            return False
        db.delete(tx)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print("[ERROR] delete_transaction:", e)
        raise
    finally:
        db.close()
