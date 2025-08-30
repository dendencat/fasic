from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_record_swipe():
    response = client.post("/swipes/", params={"user_id": "user1", "track_id": 1, "liked": True})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Swipe recorded"
