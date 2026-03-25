import threading
import uuid
import asyncio

jobs = {}
subscribers = {}  # job_id → [websockets]
event_loop = None

# -------------------------------
# Job Structure
# -------------------------------
class JobStatus:
    def __init__(self):
        self.status = "pending"
        self.result = None
        self.error = None
        self.progress = 0
        self.current_step = None
        


# -------------------------------
# WebSocket Subscription
# -------------------------------
def subscribe(job_id, websocket):
    if job_id not in subscribers:
        subscribers[job_id] = []

    subscribers[job_id].append(websocket)


def unsubscribe(job_id, websocket):
    if job_id in subscribers:
        if websocket in subscribers[job_id]:
            subscribers[job_id].remove(websocket)

def set_event_loop(loop):
    global event_loop
    event_loop = loop

async def notify(job_id):
    if job_id not in subscribers:
        return

    job = jobs.get(job_id)
    if not job:
        return

    for ws in list(subscribers[job_id]):
        try:
            await ws.send_json({
                "job_id": job_id,
                "status": job.status,
                "progress": job.progress,
                "current_step": job.current_step,
                "result": job.result,
                "error": job.error
            })
        except Exception:
            pass


def safe_notify(job_id):
    if event_loop is None:
        return

    asyncio.run_coroutine_threadsafe(notify(job_id), event_loop)


# -------------------------------
# Background Execution
# -------------------------------
def run_in_background(job_id, func, *args, **kwargs):
    job = jobs[job_id]

    try:
        job.status = "running"
        safe_notify(job_id)

        # 🔥 IMPORTANT: pass job + job_id
        result = func(job, job_id, *args, **kwargs)

        job.status = "completed"
        job.result = result
        job.progress = 100

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        print("ERROR:", e)

    finally:
        safe_notify(job_id)


def submit_job(func, *args, **kwargs):
    job_id = str(uuid.uuid4())

    jobs[job_id] = JobStatus()

    thread = threading.Thread(
        target=run_in_background,
        args=(job_id, func, *args),
        kwargs=kwargs,
        daemon=True
    )

    thread.start()

    return job_id


def get_job(job_id):
    return jobs.get(job_id)


def get_all_jobs():
    return jobs