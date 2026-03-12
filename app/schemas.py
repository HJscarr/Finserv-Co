from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AccountCreate(BaseModel):
    owner_name: str
    email: str
    balance: Optional[float] = 0.0


class AccountResponse(BaseModel):
    id: int
    owner_name: str
    email: str
    balance: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    transaction_type: str
    description: Optional[str] = ""


class TransactionResponse(BaseModel):
    id: int
    account_id: int
    amount: float
    transaction_type: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


class PortfolioItemCreate(BaseModel):
    account_id: int
    ticker: str
    shares: float
    purchase_price: float
    current_price: float


class PortfolioItemResponse(BaseModel):
    id: int
    account_id: int
    ticker: str
    shares: float
    purchase_price: float
    current_price: float

    class Config:
        from_attributes = True


class PortfolioSummary(BaseModel):
    account_id: int
    total_value: float
    total_gain_loss: float
    gain_loss_percentage: float
    items: list[PortfolioItemResponse]
