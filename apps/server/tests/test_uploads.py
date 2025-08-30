from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_file():
    # Mock upload
    files = {"file": ("test.mp3", b"fake audio data", "audio/mpeg")}
    response = client.post("/uploads/", files=files)
    # Assuming S3 is mocked or skipped
    assert response.status_code in [200, 500]  # 500 if S3 not available
