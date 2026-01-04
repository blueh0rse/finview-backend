from sqlalchemy import case, func
from src.api.db.db import SessionLocal
from src.api.schemas.transactions import OperationEnum, TransactionORM


async def calc_portfolio_value() -> float:
    print("[portfolio] CALC VALUE")
    db = SessionLocal()
    try:
        buy_total = (
            db.query(func.sum(TransactionORM.amount))
            .filter(TransactionORM.operation == OperationEnum.BUY.value)
            .scalar()
            or 0
        )
        sell_total = (
            db.query(func.sum(TransactionORM.amount))
            .filter(TransactionORM.operation == OperationEnum.SELL.value)
            .scalar()
            or 0
        )

        total_value = buy_total - sell_total
        return float(total_value)
    finally:
        db.close()


async def calc_portfolio_allocation():
    print("[portfolio] CALC ALLOCATION")
    db = SessionLocal()
    try:
        # net quantity
        results = (
            db.query(
                TransactionORM.asset,
                func.sum(
                    case(
                        (
                            TransactionORM.operation == OperationEnum.BUY.value,
                            TransactionORM.quantity,
                        ),
                        (
                            TransactionORM.operation == OperationEnum.SELL.value,
                            -TransactionORM.quantity,
                        ),
                        else_=0,
                    )
                ).label("net_quantity"),
                func.avg(TransactionORM.unit_price).label("avg_unit_price"),
            )
            .group_by(TransactionORM.asset)
            .all()
        )

        # total value per asset
        allocation = []
        total_value = 0
        for asset, qty, avg_price in results:
            if qty and qty > 0:
                value = qty * avg_price
                total_value += value
                allocation.append({"asset": asset, "value": value})

        # calculate percentages
        for a in allocation:
            a["percent"] = round(a["value"] / total_value * 100, 2)

        return total_value, allocation
    finally:
        db.close()
