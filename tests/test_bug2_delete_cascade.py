"""
Bug 2: Deleting an account with linked transactions/portfolio items fails.

The API should either cascade-delete related records or return a 409 Conflict,
rather than crashing with a foreign key constraint error.
"""


def test_delete_account_with_transactions_succeeds(client):
    """Deleting an account that has transactions should not raise a 500."""
    # Create account
    acct = client.post("/accounts/", json={
        "owner_name": "Bob", "email": "bob@example.com", "balance": 1000.0
    }).json()

    # Create a transaction linked to the account
    client.post("/transactions/", json={
        "account_id": acct["id"],
        "amount": 100.0,
        "transaction_type": "deposit",
    })

    # Delete should succeed (cascade) or return 409, not 500
    resp = client.delete(f"/accounts/{acct['id']}")
    assert resp.status_code != 500, (
        "Deleting an account with linked transactions should not return 500"
    )


def test_delete_account_with_portfolio_items_succeeds(client):
    """Deleting an account that has portfolio items should not raise a 500."""
    # Create account
    acct = client.post("/accounts/", json={
        "owner_name": "Carol", "email": "carol@example.com", "balance": 5000.0
    }).json()

    # Create a portfolio item linked to the account
    client.post("/portfolio/", json={
        "account_id": acct["id"],
        "ticker": "AAPL",
        "shares": 10.0,
        "purchase_price": 150.0,
        "current_price": 175.0,
    })

    # Delete should succeed (cascade) or return 409, not 500
    resp = client.delete(f"/accounts/{acct['id']}")
    assert resp.status_code != 500, (
        "Deleting an account with linked portfolio items should not return 500"
    )
