from api.db.db import engine, Base
from api.schemas.transactions import TransactionORM

print("[LOG] Creating tables...")
Base.metadata.create_all(bind=engine)
print("[LOG] Tables created successfully.")
