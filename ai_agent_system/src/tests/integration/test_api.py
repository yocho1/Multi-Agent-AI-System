from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.utils.auth import create_access_token

client = TestClient(app)


def test_health():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] in {"ok", "degraded"}


def test_metrics():
    resp = client.get("/api/v1/metrics")
    assert resp.status_code == 200


def test_auth_token():
    resp = client.post("/api/v1/auth/token", json={"username": "demo", "password": "demo"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_auth_invalid():
    resp = client.post("/api/v1/auth/token", json={"username": "bad", "password": "bad"})
    assert resp.status_code == 401


def test_agents_list_with_auth():
    token = create_access_token({"sub": "test"})
    resp = client.get("/api/v1/agents", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
