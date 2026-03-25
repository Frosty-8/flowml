from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from flowml.runtime.state import registry
import asyncio
from flowml.runtime.scheduler import subscribe, unsubscribe, get_job

router = APIRouter()

@router.websocket("/ws/metrics")
async def metrics_ws(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected ✅")

    try:
        while True:
            data = {
                "requests": registry.metrics_engine.get_request_metrics(),
                "data": registry.metrics_engine.get_data_metrics(),
                "cleaning": registry.metrics_engine.get_cleaning_metrics()
            }

            await websocket.send_json(data)
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("Client disconnected 🔌")

    except RuntimeError as e:
        print("Socket already closed:", e)

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        print("WebSocket closed ❌")

@router.websocket("/ws/job/{job_id}")
async def job_ws(websocket: WebSocket, job_id: str):
    await websocket.accept()

    subscribe(job_id, websocket)

    # 🔥 SEND INITIAL STATE (IMPORTANT FIX)
    job = get_job(job_id)
    if job:
        await websocket.send_json({
            "job_id": job_id,
            "status": job.status,
            "progress": job.progress,
            "current_step": job.current_step,
            "result": job.result,
            "error": job.error
        })

    try:
        while True:
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        unsubscribe(job_id, websocket)