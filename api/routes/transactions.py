from typing import List
import uuid
from fastapi import APIRouter
from fastapi import HTTPException
from api.models.transactions import Transaction, TransactionCreate
from api.services.transactions import (
    create_one_transaction,
    delete_one_transaction,
    get_all_transactions,
    get_transaction_by_id,
)

router = APIRouter(tags=["Transactions"])


@router.get("/transactions", response_model=List[Transaction])
async def get_transactions():
    """Retrieve all transactions"""
    print("[REQ] GET /transactions")
    transactions = await get_all_transactions()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
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
    print(
        f"[REQ] POST /transactions {transaction.asset} - {transaction.operation} - {transaction.amount}{transaction.currency}"
    )
    created_transaction = await create_one_transaction(transaction)
    if created_transaction is None:
        raise HTTPException(status_code=400, detail="Failed to create transaction")
    return created_transaction


@router.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: uuid.UUID):
    print(f"[REQ] DELETE /transactions/{transaction_id}")
    deleted = await delete_one_transaction(transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return deleted
