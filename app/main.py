from fastapi import FastAPI

from app.database import Base, engine
from app.routers import accounts, transactions, portfolio

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spot Fintech API",
    description="Internal API for FinServ Co account and portfolio management",
    version="1.0.0",
)

app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(portfolio.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
