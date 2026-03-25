from fastapi import APIRouter, HTTPException
from flowml.storage.sqlite import get_dataset
from flowml.runtime.state import registry
from flowml.rust_bridge.bridge import fast_drop_nulls, fast_fill_nulls
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/drop_nulls")
def drop_nulls(dataset_id: str):
    try:
        dataset = get_dataset(dataset_id)

        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")

        path = dataset["path"]

        output_path, kept = fast_drop_nulls(path)

        registry.metrics_engine.log_cleaning(
            {"operation": "drop_nulls_rust", "rows_after": kept}
        )

        return {
            "message": "Processed via Rust",
            "output_path": output_path,
            "rows_after": kept,
        }

    except Exception as e:
        logger.exception("Drop nulls failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fill_nulls")
def fill_nulls(dataset_id: str, value: str = "0"):
    try:
        dataset = get_dataset(dataset_id)

        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")

        path = dataset["path"]

        output_path = fast_fill_nulls(path, value)

        registry.metrics_engine.log_cleaning({"operation": "fill_nulls_rust"})

        return {"message": "Processed via Rust", "output_path": output_path}

    except Exception as e:
        logger.exception("Fill nulls failed")
        raise HTTPException(status_code=500, detail=str(e))
