"""
Bug 4: Querying transactions for a non-existent account returns 200 with [].

The API should return a 404 Not Found when the account does not exist,
rather than silently returning an empty list.
"""


def test_transactions_for_nonexistent_account_returns_404(client):
    """GET /transactions/{id} should return 404 for a non-existent account."""
    resp = client.get("/transactions/99999")
    assert resp.status_code == 404, (
        f"Expected 404 for non-existent account, got {resp.status_code}"
    )
