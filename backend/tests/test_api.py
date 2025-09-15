# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_load_team1():
    response = client.get("/loadTeam/team1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6
    for poke in data:
        assert "family" in poke
        assert "hp" in poke
