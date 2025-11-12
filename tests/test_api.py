"""
Testes da API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Testa endpoint raiz (frontend HTML)"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "<!DOCTYPE html>" in response.text or "<html" in response.text.lower()


def test_api_root():
    """Testa endpoint /api"""
    response = client.get("/api")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Testa health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_subjects():
    """Testa endpoint de disciplinas"""
    response = client.get("/api/v1/subjects")
    assert response.status_code == 200
    assert "subjects" in response.json()
    assert isinstance(response.json()["subjects"], list)


def test_chat_endpoint_missing_message():
    """Testa endpoint de chat sem mensagem"""
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422  # Validation error

