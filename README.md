# 🎬 Video Downloader API

A containerized FastAPI service that accepts video download requests, queues them, and processes them asynchronously. This project is designed to demonstrate both software engineering, and quality engineering practices.

---

## 🚀 What this project demonstrates
- REST API design with FastAPI
- Background job processing using threads
- Lightweight browser UI for manual submission
- End-to-end test coverage with API tests, UI smoke tests, and Selenium browser automation
- CI pipeline using GitHub Actions
- Docker-based packaging for reproducible deployment

---

## 🧱 Tech stack
- Python 3.11
- FastAPI
- Docker
- GitHub Actions
- Selenium + WebDriver manager
- pytest

---

## 🧪 Testing coverage
- `tests/test_api.py` covers the API endpoints:
  - `GET /`
  - `POST /download`
  - `GET /status/{job_id}`
- `tests/test_ui.py` verifies the browser UI page and form submission behavior
- `tests/test_selenium.py` runs a headless Chrome browser against `/ui`, submits the form, and confirms a `job_id` is returned
- External download behavior is isolated by mocking thread startup during unit tests

---

## 🔁 CI/CD workflow
The GitHub Actions workflow includes:
- dependency installation
- API and UI unit tests
- Docker image build
- dedicated Selenium browser test job


---

## 📚 Project structure
- `app/main.py` - FastAPI application and UI route
- `app/worker.py` - background job processor
- `Dockerfile` - container definition
- `tests/` - API, UI, and Selenium test coverage
- `.github/workflows/ci.yml` - CI pipeline configuration

---

## 🔮 Notes
- Storage is in memory, so jobs are lost on server restart
- Pytube can be be unreliable due to YouTube changes
- Selenium is included to demonstrate browser-level validation and CI reliability but the UI isn't fully developed.

