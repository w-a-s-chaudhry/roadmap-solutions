# Author:      Wajid Ali Chaudhry
# Description: Tests for /todos CRUD endpoints.

import pytest
from fastapi.testclient import TestClient


# --- Fixtures ---


@pytest.fixture
def auth_headers(client: TestClient) -> dict:
    client.post(
        "/auth/register", json={"email": "test@gmail.com", "password": "Password1"}
    )
    response = client.post(
        "/auth/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    access_token = response.json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth_headers_b(client: TestClient) -> dict:
    client.post(
        "/auth/register", json={"email": "test_b@gmail.com", "password": "Password1"}
    )
    response = client.post(
        "/auth/login", json={"email": "test_b@gmail.com", "password": "Password1"}
    )
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


# --- Create ---


def test_create_todo(client: TestClient, auth_headers: dict):
    response = client.post("/todos", json={"title": "Buy milk"}, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["title"] == "Buy milk"


def test_create_todo_unauthenticated(client: TestClient):
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 401


# --- List ---


def test_list_todos(client: TestClient, auth_headers: dict):
    client.post("/todos", json={"title": "tasks_a"}, headers=auth_headers)
    response = client.post("/todos", json={"title": "tasks_b"}, headers=auth_headers)
    assert response.status_code == 201
    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2


# --- Get one ---


def test_get_todo(client: TestClient, auth_headers: dict):
    todo_id = client.post(
        "/todos", json={"title": "task"}, headers=auth_headers
    ).json()["id"]
    response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 200


def test_get_todo_not_found(client: TestClient, auth_headers: dict):
    response = client.get("/todos/9999", headers=auth_headers)
    assert response.status_code == 404


# --- Update ---


def test_update_todo(client: TestClient, auth_headers: dict):
    todo_id = client.post(
        "/todos", json={"title": "task"}, headers=auth_headers
    ).json()["id"]
    response = client.patch(
        f"/todos/{todo_id}", json={"done": True}, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["done"]


# --- Delete ---


def test_delete_todo(client: TestClient, auth_headers: dict):
    todo_id = client.post(
        "/todos", json={"title": "task"}, headers=auth_headers
    ).json()["id"]
    response = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 404


# --- Ownership ---


def test_ownership_get(
    client: TestClient,
    auth_headers: dict,
    auth_headers_b: dict,
):
    todo_id = client.post(
        "/todos", json={"title": "task"}, headers=auth_headers
    ).json()["id"]
    response = client.get(f"/todos/{todo_id}", headers=auth_headers_b)
    assert response.status_code == 404
