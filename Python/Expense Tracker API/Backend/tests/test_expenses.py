# Author:      Wajid Ali Chaudhry
# Description: Tests for expense endpoints — CRUD, ownership,
#              filtering, pagination, and summary.

import pytest
from datetime import date, timedelta

# --- Constants ---

REGISTER_URL = "/auth/register"
LOGIN_URL    = "/auth/login"
EXPENSES_URL = "/expenses"
SUMMARY_URL  = "/expenses/summary"

TODAY     = str(date.today())
LAST_WEEK = str(date.today() - timedelta(days=3))
LONG_AGO  = str(date.today() - timedelta(days=120))


# --- Fixtures ---

# Register Alice and return her Bearer headers
@pytest.fixture
def auth_headers(client):
    client.post(REGISTER_URL, json={
        "name": "Alice", "email": "alice@example.com", "password": "pass123",
    })
    token = client.post(LOGIN_URL, json={
        "email": "alice@example.com", "password": "pass123",
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# Register Bob and return his Bearer headers (for ownership tests)
@pytest.fixture
def other_headers(client):
    client.post(REGISTER_URL, json={
        "name": "Bob", "email": "bob@example.com", "password": "pass456",
    })
    token = client.post(LOGIN_URL, json={
        "email": "bob@example.com", "password": "pass456",
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# --- Helpers ---

# Post a single expense and return its response JSON
def make_expense(client, headers, **overrides):
    payload = {
        "title": "Coffee",
        "amount": 4.50,
        "category": "food",
        "date": TODAY,
    }
    payload.update(overrides)
    return client.post(EXPENSES_URL, json=payload, headers=headers).json()


# --- CRUD ---

# Creating an expense returns 201 and the saved data
def test_create_expense(client, auth_headers):
    res = client.post(EXPENSES_URL, json={
        "title": "Groceries",
        "amount": 32.00,
        "category": "food",
        "date": TODAY,
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Groceries"
    assert float(data["amount"]) == 32.00
    assert data["category"] == "food"
    assert "id" in data


# Fetching by id returns the same data
def test_get_expense(client, auth_headers):
    created = make_expense(client, auth_headers)
    res = client.get(f"{EXPENSES_URL}/{created['id']}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["title"] == created["title"]


# PATCH updates only the sent fields
def test_update_expense(client, auth_headers):
    created = make_expense(client, auth_headers)
    res = client.patch(
        f"{EXPENSES_URL}/{created['id']}",
        json={"title": "Updated title"},
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert res.json()["title"] == "Updated title"
    assert float(res.json()["amount"]) == float(created["amount"])


# DELETE returns 204; subsequent GET returns 404
def test_delete_expense(client, auth_headers):
    created = make_expense(client, auth_headers)
    del_res = client.delete(
        f"{EXPENSES_URL}/{created['id']}", headers=auth_headers
    )
    assert del_res.status_code == 204
    get_res = client.get(
        f"{EXPENSES_URL}/{created['id']}", headers=auth_headers
    )
    assert get_res.status_code == 404


# --- Ownership ---

# Another user cannot read Alice's expense
def test_get_expense_wrong_owner(client, auth_headers, other_headers):
    created = make_expense(client, auth_headers)
    res = client.get(
        f"{EXPENSES_URL}/{created['id']}", headers=other_headers
    )
    assert res.status_code == 404


# Another user cannot delete Alice's expense; it still exists for Alice
def test_delete_expense_wrong_owner(client, auth_headers, other_headers):
    created = make_expense(client, auth_headers)
    del_res = client.delete(
        f"{EXPENSES_URL}/{created['id']}", headers=other_headers
    )
    assert del_res.status_code == 404
    still_there = client.get(
        f"{EXPENSES_URL}/{created['id']}", headers=auth_headers
    )
    assert still_there.status_code == 200


# --- List / filtering ---

# Default range returns a paginated response shape
def test_list_default_range(client, auth_headers):
    make_expense(client, auth_headers)
    res = client.get(EXPENSES_URL, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


# Expenses older than the range window are excluded
def test_list_excludes_old_expenses(client, auth_headers):
    make_expense(client, auth_headers, date=LONG_AGO)
    make_expense(client, auth_headers, date=TODAY)
    res = client.get(
        EXPENSES_URL, params={"range": "past_month"}, headers=auth_headers
    )
    assert res.json()["total"] == 1


# Category filter returns only matching expenses
def test_list_category_filter(client, auth_headers):
    make_expense(client, auth_headers, category="food")
    make_expense(client, auth_headers, category="transport")
    res = client.get(
        EXPENSES_URL, params={"category": "food"}, headers=auth_headers
    )
    data = res.json()
    assert data["total"] == 1
    assert data["items"][0]["category"] == "food"


# Custom range with explicit dates returns expenses within the window
def test_list_custom_range(client, auth_headers):
    make_expense(client, auth_headers, date=LAST_WEEK)
    res = client.get(
        EXPENSES_URL,
        params={"range": "custom", "start_date": LAST_WEEK, "end_date": TODAY},
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert res.json()["total"] >= 1


# Custom range without dates returns 422
def test_list_custom_range_missing_dates(client, auth_headers):
    res = client.get(
        EXPENSES_URL, params={"range": "custom"}, headers=auth_headers
    )
    assert res.status_code == 422


# No auth header → 401
def test_list_unauthenticated(client):
    res = client.get(EXPENSES_URL)
    assert res.status_code == 401


# --- Summary ---

# No expenses → zero totals and no top category
def test_summary_empty(client, auth_headers):
    res = client.get(SUMMARY_URL, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert float(data["total_spent"]) == 0
    assert data["count"] == 0
    assert data["top_category"] is None


# Two expenses → correct count, total, and top category
def test_summary_counts(client, auth_headers):
    make_expense(client, auth_headers, category="food", amount=10.00)
    make_expense(client, auth_headers, category="transport", amount=5.00)
    res = client.get(SUMMARY_URL, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 2
    assert float(data["total_spent"]) == 15.00
    assert data["top_category"] == "food"


# Summary only counts expenses within the requested range
def test_summary_range_exclusion(client, auth_headers):
    make_expense(client, auth_headers, date=LONG_AGO, amount=99.00)
    make_expense(client, auth_headers, date=TODAY, amount=5.00)
    res = client.get(
        SUMMARY_URL, params={"range": "past_month"}, headers=auth_headers
    )
    data = res.json()
    assert data["count"] == 1
    assert float(data["total_spent"]) == 5.00
