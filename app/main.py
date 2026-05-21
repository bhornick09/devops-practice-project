from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from uuid import uuid4
import threading
from app.worker import process_job

app = FastAPI()

# In-memory database to store job states, when the server restarts these are lost
jobs = {}

@app.get("/")
def root():
    # Check to ensure API is running
    return {"message": "Video Downloader API is running"}

@app.get("/ui", response_class=HTMLResponse)
def ui():
    # Simple HTML page with a form to submit video download requests
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>Video Downloader UI</title>
      </head>
      <body>
        <h1>Video Downloader</h1>
        <p>Submit a YouTube URL to start a download job.</p>
        <form action="/download" method="post">
          <label for="url">Video URL</label><br />
          <input id="url" name="url" type="url" placeholder="https://..." required />
          <button type="submit">Start download</button>
        </form>
      </body>
    </html>
    """

@app.post("/download")
def download_video(url: str = Form(...)):
    # Receive the URL from a form submission or POST body

    # Generate a unique ID for this request
    job_id = str(uuid4())

    # Initialize the new job entry with a queued status
    jobs[job_id] = {"status": "queued", "url": url}

    # Start the background thread for downloading
    thread = threading.Thread(target=process_job, args=(job_id, jobs))
    thread.start()

    # Return the Job ID so the caller can track status
    return {"job_id": job_id}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    return jobs.get(job_id, {"error": "Job not found"})

