from api.db.db import engine, Base

print("[LOG] Creating tables...")
Base.metadata.create_all(bind=engine)
print("[LOG] Tables created successfully.")
