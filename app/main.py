from fastapi import FastAPI
from uuid import uuid4
import threading
from app.worker import process_job

app = FastAPI()

# In-memory database to store job states
# when server restarts these are lost
jobs = {} 

@app.get("/")
def root():
    #Check to ensure API is running
    return {"message" : "Video Downloader API is running"}

@app.post("/download")
def download_video(url: str):
    # This receives a URL and starts a background thread to download
    
    #Generate a unique ID for this request
    job_id = str(uuid4())

    # Initialize the new job entry with a queued status
    # Makes jobs dict a dict of dicts
    jobs[job_id] = {"status": "queued", "url": url}

    # Actually start the background thread for downloading
    thread = threading.Thread(target=process_job, args=(job_id, jobs))
    thread.start()

    # Return the Job ID so it is shown that the job started
    return {"job_id": job_id}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    return jobs.get(job_id, {"error": "Job not found"})

