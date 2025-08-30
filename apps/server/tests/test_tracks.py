from fastapi.testclient import TestClient
from app.main import app
from app.db import init_engine
from app.models import Base

client = TestClient(app)


def setup_module():
    # Create tables
    engine = init_engine()
    Base.metadata.create_all(bind=engine)


def test_get_tracks():
    response = client.get("/tracks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_track():
    response = client.post("/tracks/", params={"title": "Test Track", "artist": "Test Artist", "genre": "Pop"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Track created"
