import time
def process_job(job_id, jobs):
    jobs[job_id]["status"] = "processing"
    time.sleep(5)  # Simulate time-consuming task
    jobs[job_id]["status"] = "completed"