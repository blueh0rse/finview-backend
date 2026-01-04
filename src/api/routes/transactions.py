from typing import List
import uuid
from fastapi import APIRouter
from fastapi import HTTPException
from src.api.models.transactions import Transaction, TransactionCreate, TransactionUpdate
from src.api.services.transactions import (
    create_one_transaction,
    delete_one_transaction,
    get_all_transactions,
    get_transaction_by_id,
    update_one_transaction,
)

router = APIRouter(tags=["Transactions"])


@router.get("/transactions", response_model=List[Transaction])
async def get_transactions(skip: int = 0, limit: int = 10):
    """Retrieve all transactions"""
    print("[REQ] GET /transactions")
    transactions = await get_all_transactions(skip, limit)
    if not transactions:
        raise HTTPException(status_code=204)
    return transactions


@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: uuid.UUID):
    """Retrieve a specific transaction by ID"""
    print(f"[REQ] GET /transactions/{transaction_id}")
    transaction = await get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("/transactions", response_model=Transaction, status_code=201)
async def create_transaction(transaction: TransactionCreate):
    """Create a new transaction"""
    print(
        f"[REQ] POST /transactions {transaction.asset_symbol} - {transaction.operation} - {transaction.amount}{transaction.currency}"
    )
    created_transaction = await create_one_transaction(transaction)
    if created_transaction is None:
        raise HTTPException(status_code=400, detail="Failed to create transaction")
    return created_transaction


@router.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(transaction_id: uuid.UUID, transaction: TransactionUpdate):
    """Update an existing transaction by ID"""
    print(f"[REQ] PUT /transactions/{transaction_id}")
    existing_transaction = await get_transaction_by_id(transaction_id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # merge existing data with updates
    updates = transaction.model_dump(exclude_unset=True)
    updated_data = existing_transaction.model_dump()
    updated_data.update(updates)

    updated_transaction = Transaction(**updated_data)

    result = await update_one_transaction(updated_transaction)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to update transaction")
    return result


@router.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: uuid.UUID):
    """Delete a specific transaction by ID"""
    print(f"[REQ] DELETE /transactions/{transaction_id}")
    deleted = await delete_one_transaction(transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return deleted
