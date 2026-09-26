from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_system_contains_cpu_and_memory():
    data = client.get("/api/system").json()
    assert "cpu_percent" in data
    assert "memory" in data


def test_storage_has_usage():
    data = client.get("/api/storage").json()
    assert data["total_bytes"] > 0
    assert 0 <= data["percent"] <= 100


def test_network_has_interfaces():
    data = client.get("/api/network").json()
    assert "interfaces" in data