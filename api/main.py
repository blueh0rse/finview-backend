from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import portfolio, transactions
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)
app.include_router(portfolio.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
