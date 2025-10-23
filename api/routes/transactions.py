from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from api.models.transactions import Transaction
from api.services.transactions import get_all_transactions

router = APIRouter(tags=["Transactions"])


@router.get("/transactions", response_model=List[Transaction])
async def get_transactions():
    """Retrieve all transactions"""
    print("[LOG] GET /transactions")
    transactions = await get_all_transactions()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return transactions
