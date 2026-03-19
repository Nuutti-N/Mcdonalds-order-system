
import pytest
from fastapi.testclient import TestClient
from main import app  # issue, solve soon

client = TestClient(app)

# Test for welcome endpoint


def test_welcome():
    response = client.get("/MCDONALDS")
    assert response.status_code == 200
    assert response.json() == {
        "Message": "Welcome to McDonald's Order system."}

# Test for user authentication endpoints


def test_signup():
    response = client.post(
        "/Signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["detail"] == "Username exists"


def test_login():
    response = client.post(
        "/Login", data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fail():
    response = client.post(
        "/Login", data={"username": "piupau", "password": "piupau23"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect Username or password"


def test_get_me():
    login = client.post(
        "/Login", data={"username": "testuser", "password": "testpass"})
    token = login.json()["access_token"]
    response = client.get("/Me", headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    assert data["username"]
    assert response.status_code == 200
    assert isinstance(data["id"], int)


# Test for order endpoints

def test_create_order():
    login = client.post(
        "/Login", data={"username": "testuser", "password": "testpass"}
    )
    token = login.json()["access_token"]
    response = client.post(
        "/order", headers={"Authorization": f"Bearer {token}"}, json={"item": "Big mac", "price": 5.99})
    assert response.status_code == 200
    data = response.json()
    assert data["Message"] == "Order added successfully"
    assert data["order"]["item"] == "Big mac"
    assert data["order"]["price"] == 5.99


def test_delete_order():
    login = client.post(
        "/Login", data={"username": "testuser", "password": "testpass"}
    )
    token = login.json()["access_token"]
    create_response = client.post(
        "/order", headers={"Authorization": f"Bearer {token}"}, json={"item": "Big mac", "price": 5.99})
    created = create_response.json()
    order_id = created["order"]["id"]
    response = client.delete(
        f"/order/{order_id}", headers={"Authorization": f"Bearer {token}"})
    created = response.json()
    assert response.status_code == 200
    assert created["Message"] == "Item deleted successfully"


def test_order_pending():
    response = client.get(
        "/order/pending"
    )
    assert response.status_code == 200
    assert response.json()

# Test for Goodbye endpoint


def test_read_main():
    response = client.get("/Goodbye")
    assert response.status_code == 200
    assert response.json() == {
        "Message": "Thank you for visiting, and welcome back."}
