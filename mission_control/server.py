from fastapi import FastAPI, Query
from mission_control.jobs import JobManager
from mission_control.openclaw_adapter import get_status, run_job

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.get("/api/status")
def status(deep: bool = Query(False)):
    if deep:
        return get_status("--deep")
    return get_status()

@app.post("/api/run")
def run(args: str):
    return run_job(args.split())

@app.get("/api/jobs")
def list_jobs():
    return JobManager.list_jobs()

@app.get("/api/jobs/{job_id}")
def job_details(job_id: str):
    return JobManager.get_job(job_id)