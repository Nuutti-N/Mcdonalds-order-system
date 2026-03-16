import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/Signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
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
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect Username or password"


def test_welcome():
    response = client.get("/MCDONALDS")
    assert response.status_code == 200
    assert response.json() == {
        "Message": "Welcome to McDonald's Order system."}


def test_read_main():
    response = client.get("/Welcome")
    assert response.status_code == 200
    assert response.json() == {
        "Message": "Thank you for visiting, and welcome back."}
