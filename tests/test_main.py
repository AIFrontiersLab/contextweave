"""Tests for Prompt Refiner MVP."""
import pytest
from fastapi.testclient import TestClient
from main import app, refine_prompt_text, execute_prompt

client = TestClient(app)


def test_refine_no_history():
    """Test refinement without history."""
    res = client.post("/refine", json={"prompt": "Test", "history": []})
    assert res.status_code == 200
    data = res.json()
    assert "Add previous context for better results" in data["suggestions"]


def test_refine_with_history():
    """Test refinement with history."""
    res = client.post("/refine", json={"prompt": "Test", "history": ["prev"]})
    assert res.status_code == 200
    data = res.json()
    assert "Add previous context for better results" not in data["suggestions"]


def test_execute_empty_prompt():
    """Test failure path for empty prompt."""
    res = client.post("/execute", json={"prompt": "   "})
    assert res.status_code == 400


def test_execute_valid():
    """Test successful execution."""
    res = client.post("/execute", json={"prompt": "Hello World"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "Hello World" in data["output"]
