from fastapi import APIRouter, HTTPException
from flowml.runtime.scheduler import get_job, get_all_jobs

router = APIRouter()


@router.get("/{job_id}")
def get_job_status(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "status": job.status,
        "progress": job.progress,
        "current_step": job.current_step,
        "result": job.result,
        "error": job.error
    }


@router.get("/")
def list_jobs():
    jobs = get_all_jobs()

    return {
        job_id: {
            "status": job.status,
            "progress": job.progress,
            "step": job.current_step
        }
        for job_id, job in jobs.items()
    }