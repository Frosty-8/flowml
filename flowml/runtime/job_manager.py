import threading
import uuid
from datetime import datetime


class JobManager:
    def __init__(self):
        self.jobs = {}

    def create_job(self, target, *args, **kwargs):
        job_id = str(uuid.uuid4())

        self.jobs[job_id] = {
            "status": "pending",
            "result": None,
            "error": None,
            "created_at": str(datetime.utcnow()),
            "updated_at": None,
        }

        thread = threading.Thread(
            target=self._run_job, args=(job_id, target, args, kwargs), daemon=True
        )
        thread.start()

        return job_id

    def _run_job(self, job_id, target, args, kwargs):
        self.jobs[job_id]["status"] = "running"

        try:
            result = target(*args, **kwargs)

            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["result"] = result

        except Exception as e:
            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["error"] = str(e)

        finally:
            self.jobs[job_id]["updated_at"] = str(datetime.utcnow())

    def get_job(self, job_id):
        return self.jobs.get(job_id)
