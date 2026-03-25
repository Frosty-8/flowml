from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import logging

from flowml.runtime.pipeline import PipelineEngine
from flowml.runtime.scheduler import submit_job, get_job

router = APIRouter()
engine = PipelineEngine()

logger = logging.getLogger(__name__)


# ----------------------------
# Request Schema
# ----------------------------
class PipelineRequest(BaseModel):
    dataset_id: str = Field(..., description="Dataset ID")
    steps: List[Dict[str, Any]] = Field(..., description="Pipeline steps")


# ----------------------------
# Run Pipeline (ASYNC)
# ----------------------------
@router.post("/run")
def run_pipeline(request: PipelineRequest):
    try:
        if not request.steps:
            raise HTTPException(status_code=400, detail="No pipeline steps provided")

        job_id = submit_job(
            engine.run,
            request.dataset_id,
            request.steps
        )

        logger.info(f"Pipeline job submitted: {job_id}")

        return {
            "message": "Pipeline started",
            "job_id": job_id,
            "status": "pending"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Pipeline submission failed")
        raise HTTPException(status_code=500, detail="Pipeline submission failed")


# ----------------------------
# Get Job Status (fallback API)
# ----------------------------
@router.get("/status/{job_id}")
def job_status(job_id: str):
    try:
        job = get_job(job_id)

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return {
            "job_id": job_id,
            "status": job.status,
            "progress": job.progress,
            "current_step": job.current_step,
            "result": job.result if job.status == "completed" else None,
            "error": job.error if job.status == "failed" else None
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Failed to fetch job status")
        raise HTTPException(status_code=500, detail="Failed to fetch job status")