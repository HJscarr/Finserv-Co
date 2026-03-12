from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Account, Transaction
from app.schemas import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse)
def create_transaction(txn: TransactionCreate, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == txn.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if txn.transaction_type == "withdrawal":
        # BUG 3: Balance goes negative - no check that the account has
        # sufficient funds before processing a withdrawal.
        account.balance -= txn.amount
    elif txn.transaction_type == "deposit":
        account.balance += txn.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    db_txn = Transaction(
        account_id=txn.account_id,
        amount=txn.amount,
        transaction_type=txn.transaction_type,
        description=txn.description,
    )
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn


@router.get("/{account_id}", response_model=list[TransactionResponse])
def get_transactions(account_id: int, db: Session = Depends(get_db)):
    # BUG 4: No validation that the account exists before querying
    # transactions. Returns an empty list for non-existent accounts
    # instead of a 404, which is misleading to API consumers.
    transactions = (
        db.query(Transaction)
        .filter(Transaction.account_id == account_id)
        .all()
    )
    return transactions
