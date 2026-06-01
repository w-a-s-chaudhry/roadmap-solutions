# Author:      Wajid Ali Chaudhry
# Description: Tests for /auth/register, /auth/login, /auth/refresh.

from fastapi.testclient import TestClient


# --- Register ---


def test_register_success(client: TestClient):
    response = client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["email"]


def test_register_duplicate_email(client: TestClient):
    client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    response = client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 409


# --- Login ---


def test_login_success(client: TestClient):
    client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    response = client.post(
        "/auth/login", json={"email": "test@gmail.com", "password": "Password1"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"]


def test_login_wrong_password(client: TestClient):
    client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    response = client.post(
        "/auth/login", json={"email": "test@gmail.com", "password": "Password2"}
    )
    assert response.status_code == 401


def test_login_unknown_email(client: TestClient):
    response = client.post(
        "/auth/login", json={"email": "test@gmail.com", "password": "Password2"}
    )
    assert response.status_code == 401


# --- Refresh ---


def test_refresh_success(client: TestClient):
    client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    response = client.post(
        "/auth/login", json={"email": "test@gmail.com", "password": "Password1"}
    )

    data = response.json()
    refresh_token = data["refresh_token"]

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_refresh_with_access_token(client: TestClient):
    client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    response = client.post(
        "/auth/login", json={"email": "test@gmail.com", "password": "Password1"}
    )

    data = response.json()
    access_token = data["access_token"]

    response = client.post("/auth/refresh", json={"refresh_token": access_token})
    assert response.status_code == 401


def test_refresh_invalid_token(client: TestClient):
    response = client.post("/auth/refresh", json={"refresh_token": "garbage"})
    assert response.status_code == 401
