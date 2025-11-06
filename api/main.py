from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import transactions

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
