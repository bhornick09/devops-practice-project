from fastapi.testclient import TestClient
import app.main as main

# Create a single TestClient instance for the FastAPI app.
# The purpose of TestClient is to allow us to call app endpoints as if we were a real HTTP client.
client = TestClient(main.app)


def test_root_endpoint_returns_api_status():
    """Verify that the root API endpoint is healthy."""
    response = client.get("/")

    # The root endpoint should return a simple JSON payload
    assert response.status_code == 200
    assert response.json() == {"message": "Video Downloader API is running"}


def test_download_endpoint_creates_job(monkeypatch):
    """Verify the download endpoint creates a job and returns a job_id."""

    # The /download endpoint starts a background thread.
    # For the purpose of our tests, we don't want to actually start a thread or run pytube.
    class DummyThread:
        def __init__(self, target, args):
            self.target = target
            self.args = args

        def start(self):
            # Do nothing during the test.
            pass

    # Replace the threading. Thread class inside the app with DummyThread.
    monkeypatch.setattr(main.threading, "Thread", DummyThread)

    response = client.post("/download", data={"url": "https://example.com/video"})

    # Confirm the endpoint returns a job ID immediately.
    assert response.status_code == 200
    assert "job_id" in response.json()

    job_id = response.json()["job_id"]

    # Check that the job status is stored in the in-memory jobs dictionary.
    status_response = client.get(f"/status/{job_id}")
    assert status_response.status_code == 200
    assert status_response.json() == {"status": "queued", "url": "https://example.com/video"}


def test_status_endpoint_returns_error_for_unknown_job():
    """Verify the status endpoint returns a helpful error for missing jobs."""
    response = client.get("/status/unknown-job-id")

    # If the job ID does not exist, the API should return an error payload.
    assert response.status_code == 200
    assert response.json() == {"error": "Job not found"}
