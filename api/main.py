from fastapi import FastAPI

from api.routes import transactions

app = FastAPI()

app.include_router(transactions.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
