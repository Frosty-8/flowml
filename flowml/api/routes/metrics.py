from fastapi import APIRouter
from flowml.runtime.state import registry

router = APIRouter()


@router.get("/")
def get_metrics():
    return {
        "requests": registry.metrics_engine.get_request_metrics(),
        "data": registry.metrics_engine.get_data_metrics(),
        "cleaning": registry.metrics_engine.get_cleaning_metrics(),
    }
