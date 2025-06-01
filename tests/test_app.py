import pytest
from app.main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "OK"
    assert "message" in data

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b'app_requests_total' in response.data
