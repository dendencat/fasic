from fastapi.testclient import TestClient
from app.main import app
from app.db import init_engine
from app.models import Base

client = TestClient(app)


def setup_module():
    # Create tables
    engine = init_engine()
    Base.metadata.create_all(bind=engine)


def test_record_swipe():
    # First create a track
    response = client.post("/tracks/", params={"title": "Test Track", "artist": "Test Artist", "genre": "Pop", "s3_key": "test.mp3"})
    assert response.status_code == 200

    # Now record swipe
    response = client.post("/swipes/", params={"user_id": "user1", "track_id": 1, "liked": True})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Swipe recorded"
