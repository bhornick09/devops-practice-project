from fastapi.testclient import TestClient
import app.main as main

# We reuse the FastAPI TestClient for UI-related tests
client = TestClient(main.app)


def test_ui_page_loads_with_form():
    """Verify that the UI page loads and contains the expected form."""
    response = client.get("/ui")

    assert response.status_code == 200
    html = response.text

    # Confirm the HTML contains the download form fields and submission target
    assert "<form" in html
    assert 'action="/download"' in html
    assert 'name="url"' in html
    assert "Video Downloader" in html


def test_ui_form_can_submit_download_request(monkeypatch):
    """Verify that submitting the UI form triggers the download API endpoint."""
    class DummyThread:
        def __init__(self, target, args):
            self.target = target
            self.args = args

        def start(self):
            # Prevent background work during the test
            pass

    monkeypatch.setattr(main.threading, "Thread", DummyThread)

    response = client.post("/download", data={"url": "https://example.com/video"})

    assert response.status_code == 200
    assert "job_id" in response.json()
