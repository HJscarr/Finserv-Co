"""
Bug 5: Portfolio summary crashes with ZeroDivisionError on empty portfolio.

The API should return a valid response with 0% gain/loss when an account
has no portfolio items, rather than raising a 500 error.
"""


def test_empty_portfolio_summary_does_not_crash(client):
    """Portfolio summary for an account with no items should return 200, not 500."""
    # Create account with no portfolio items
    acct = client.post("/accounts/", json={
        "owner_name": "Frank", "email": "frank@example.com"
    }).json()

    resp = client.get(f"/portfolio/summary/{acct['id']}")
    assert resp.status_code == 200, (
        f"Expected 200 for empty portfolio summary, got {resp.status_code}"
    )


def test_empty_portfolio_gain_loss_is_zero(client):
    """An empty portfolio should report 0% gain/loss, not crash."""
    acct = client.post("/accounts/", json={
        "owner_name": "Grace", "email": "grace@example.com"
    }).json()

    resp = client.get(f"/portfolio/summary/{acct['id']}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["gain_loss_percentage"] == 0.0
    assert data["total_value"] == 0.0
    assert data["total_gain_loss"] == 0.0
