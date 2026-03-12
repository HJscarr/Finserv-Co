"""
Bug 1: Account creation allows duplicate emails.

The API should return a 409 Conflict when creating an account with an email
that already exists, rather than crashing with an unhandled database error.
"""


def test_duplicate_email_returns_409(client):
    """Creating two accounts with the same email should return 409, not 500."""
    payload = {"owner_name": "Alice", "email": "alice@example.com"}

    resp1 = client.post("/accounts/", json=payload)
    assert resp1.status_code == 200

    resp2 = client.post("/accounts/", json=payload)
    assert resp2.status_code == 409, (
        f"Expected 409 Conflict for duplicate email, got {resp2.status_code}"
    )
