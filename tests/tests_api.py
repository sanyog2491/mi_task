import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, mock_open

client = TestClient(app)

def test_upload_video():
    files = {'file': ('test_video.mkv', b'test file content', 'video/mp4')}
    response = client.post("/api/upload/", files=files)
    
    assert response.status_code == 200, f"Unexpected status code {response.status_code}. Response: {response.json()}"
    
    response_json = response.json()
    assert "id" in response_json, f"Response did not contain 'id': {response_json}"
    assert "name" in response_json, f"Response did not contain 'name': {response_json}"
    assert "path" in response_json, f"Response did not contain 'path': {response_json}"
    assert "size" in response_json, f"Response did not contain 'size': {response_json}"
    assert "converted" in response_json, f"Response did not contain 'converted': {response_json}"

def test_search_videos():

    response = client.get("/api/search/", params={"name": "test_video.mp4"})
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
    assert len(results) > 0, f"Results: {results}"

def test_block_video():
    response = client.post("/api/block/", json={"video_id": 1})
    assert response.status_code == 200
    assert response.json() == {"message": "Video blocked from downloading."}

@pytest.mark.asyncio
async def test_download_blocked_video():
    await client.post("/api/block/", json={"video_id": 3})

    response = await client.get("/api/download/3")
    
    assert response.status_code == 403
    assert response.json() == {"detail": "Video is blocked for download."}


def test_download_non_blocked_video():
    response = client.get("/api/download/3")
    assert response.status_code == 200
    assert response.json() == {"message": "Video download started."}
