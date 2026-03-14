import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


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
