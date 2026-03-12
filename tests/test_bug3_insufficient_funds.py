"""
Bug 3: Withdrawals are processed without checking sufficient funds.

The API should return a 400 Bad Request when a withdrawal would cause the
account balance to go negative.
"""


def test_withdrawal_exceeding_balance_returns_400(client):
    """A withdrawal larger than the balance should be rejected, not processed."""
    # Create account with 100.0 balance
    acct = client.post("/accounts/", json={
        "owner_name": "Dave", "email": "dave@example.com", "balance": 100.0
    }).json()

    # Attempt to withdraw 500.0
    resp = client.post("/transactions/", json={
        "account_id": acct["id"],
        "amount": 500.0,
        "transaction_type": "withdrawal",
    })
    assert resp.status_code == 400, (
        f"Expected 400 for insufficient funds, got {resp.status_code}"
    )


def test_balance_does_not_go_negative(client):
    """Account balance should never go below zero after a withdrawal."""
    acct = client.post("/accounts/", json={
        "owner_name": "Eve", "email": "eve@example.com", "balance": 50.0
    }).json()

    # Attempt to withdraw more than the balance
    client.post("/transactions/", json={
        "account_id": acct["id"],
        "amount": 200.0,
        "transaction_type": "withdrawal",
    })

    # Verify balance did not go negative
    account = client.get(f"/accounts/{acct['id']}").json()
    assert account["balance"] >= 0, (
        f"Balance went negative: {account['balance']}"
    )
