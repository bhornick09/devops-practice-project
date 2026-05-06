from pytube import YouTube

def process_job(job_id, jobs):
    jobs[job_id]["status"] = "downloading"
    url = jobs[job_id]["url"]

    try:
        yt= Youtube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path="downloads/")
        jobs[job_id]["status"] = "completed"
    except Exception as e:
        jobs[job_id]["status"] = f"error: {str(e)}"
    