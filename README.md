# 🎬 Video Downloader API (project focused on refining DevOps skills such as Python, Docker, and CI/CD concepts)

Simple containerized Python API that queues and processes YouTube video downloads asynchronously.

---

## 🚀 Features
- Submit download jobs via API
- Track job status (queued → downloading → completed)
- Background processing with threads
- Dockerized service
- CI pipeline with GitHub Actions

---

## 🧱 Tech Stack used
- FastAPI (Python)
- Docker
- GitHub Actions
- pytube

---

## 🔁 CI/CD Skills
- GitHub Actions runs on every push:
- installs dependencies
- validates imports
- builds Docker image

## 🔮 Side notes
- In-memory job storage (no DB yet)
- Simple thread-based worker
- pytube may break occasionally

## FastAPI Documentation
FastAPI automatically generates interactive Swagger UI for testing endpoints, seen in the locally hosted screenshot below.
<img width="945" height="649" alt="image" src="https://github.com/user-attachments/assets/ec01ab6d-a953-4276-ac6c-ac8d20a8ab02" />

## Github Action Screenshot (Pass, fail, and in progress)
Github Actions automatically installs dependencies, validates my application, and builds the Docker image on every commit to the main branch.
It can be setup to react to a variety of repo changes, but in this case I've only set it up for pushes.
<img width="1312" height="399" alt="image" src="https://github.com/user-attachments/assets/17a24801-aed7-41bb-9a54-ae2a8e78f6c8" />
