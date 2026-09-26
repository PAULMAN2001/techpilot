from fastapi.testclient import TestClient

from app.diagnostics.analyzer import analyze_diagnostics
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


def test_analyzer_generates_findings():
    status, findings = analyze_diagnostics(
        {"cpu_percent": 92, "memory": {"percent": 88}},
        {"percent": 96},
        {"hostname": "test-host", "local_ip": "192.168.1.10", "interfaces": [{"name": "Ethernet"}]},
    )
    assert status == "critical"
    assert any(item["title"] == "High CPU usage" for item in findings)
    assert any(item["title"] == "Critical disk usage" for item in findings)


def test_diagnostic_run_creates_findings():
    response = client.post("/api/diagnostics/run")
    assert response.status_code == 200
    payload = response.json()
    assert "status" in payload
    assert "findings" in payload
    assert isinstance(payload["findings"], list)


def test_diagnostic_history_available():
    response = client.get("/api/diagnostics/history?limit=5")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
