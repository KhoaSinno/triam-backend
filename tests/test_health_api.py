from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok():
    response = TestClient(app).get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "triam-backend"}


def test_background_health_endpoint_uses_health_service(monkeypatch):
    monkeypatch.setattr(
        "app.api.v1.routers.health.get_background_health",
        lambda: {
            "status": "ok",
            "database": "ok",
            "redis": "ok",
            "document_queue_length": 0,
        },
    )

    response = TestClient(app).get("/api/v1/health/background")

    assert response.status_code == 200
    assert response.json()["document_queue_length"] == 0
