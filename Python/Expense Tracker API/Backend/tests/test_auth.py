# Author:      Wajid Ali Chaudhry
# Description: Tests for auth endpoints — register, login, refresh, me.

import pytest

# --- Constants ---

REGISTER_URL = "/auth/register"
LOGIN_URL    = "/auth/login"
REFRESH_URL  = "/auth/refresh"
ME_URL       = "/auth/me"

VALID_USER = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "pass123",
}


# --- Helpers ---

# Register VALID_USER and return the login response JSON
def _login(client):
    client.post(REGISTER_URL, json=VALID_USER)
    return client.post(
        LOGIN_URL,
        json={"email": VALID_USER["email"], "password": VALID_USER["password"]},
    ).json()


# Return Bearer auth headers for VALID_USER
def _auth_headers(client):
    tokens = _login(client)
    return {"Authorization": f"Bearer {tokens['access_token']}"}


# --- Register ---

# Successful registration returns 201 and the new user's data
def test_register_success(client):
    res = client.post(REGISTER_URL, json=VALID_USER)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == VALID_USER["email"]
    assert data["name"] == VALID_USER["name"]
    assert "id" in data
    assert "password" not in data


# Registering the same email twice yields 409
def test_register_duplicate_email(client):
    client.post(REGISTER_URL, json=VALID_USER)
    res = client.post(REGISTER_URL, json=VALID_USER)
    assert res.status_code == 409


# Omitting a required field yields 422
def test_register_missing_field(client):
    res = client.post(
        REGISTER_URL,
        json={"email": "no@name.com", "password": "pass123"},
    )
    assert res.status_code == 422


# --- Login ---

# Correct credentials return 200 with both token types
def test_login_success(client):
    client.post(REGISTER_URL, json=VALID_USER)
    res = client.post(
        LOGIN_URL,
        json={"email": VALID_USER["email"], "password": VALID_USER["password"]},
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


# Wrong password returns 401
def test_login_wrong_password(client):
    client.post(REGISTER_URL, json=VALID_USER)
    res = client.post(
        LOGIN_URL,
        json={"email": VALID_USER["email"], "password": "wrong"},
    )
    assert res.status_code == 401


# Unknown email returns 401
def test_login_unknown_email(client):
    res = client.post(
        LOGIN_URL,
        json={"email": "nobody@example.com", "password": "pass123"},
    )
    assert res.status_code == 401


# --- Refresh ---

# A valid refresh token returns a new token pair
def test_refresh_success(client):
    tokens = _login(client)
    res = client.post(
        REFRESH_URL, json={"refresh_token": tokens["refresh_token"]}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data


# A made-up string is rejected with 401
def test_refresh_invalid_token(client):
    res = client.post(
        REFRESH_URL, json={"refresh_token": "not.a.real.token"}
    )
    assert res.status_code == 401


# An access token used where a refresh token is expected is rejected
def test_refresh_wrong_token_type(client):
    tokens = _login(client)
    res = client.post(
        REFRESH_URL, json={"refresh_token": tokens["access_token"]}
    )
    assert res.status_code == 401


# --- Me ---

# Authenticated request returns the current user's profile
def test_get_me_authenticated(client):
    headers = _auth_headers(client)
    res = client.get(ME_URL, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == VALID_USER["email"]
    assert data["name"] == VALID_USER["name"]


# No token → 401
def test_get_me_unauthenticated(client):
    res = client.get(ME_URL)
    assert res.status_code == 401
