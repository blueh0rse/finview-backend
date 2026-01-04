from src.api.db.db import engine, Base
from src.api.schemas.assets import AssetORM
from src.api.schemas.transactions import TransactionORM

print("[LOG] Creating tables...")
Base.metadata.create_all(bind=engine)
print("[LOG] Tables created successfully.")
