from fastapi import APIRouter, HTTPException, Query
from flowml.storage.sqlite import get_dataset
from flowml.runtime.state import registry
from flowml.rust_bridge.bridge import fast_count_rows, fast_get_headers
import pandas as pd
import logging
from flowml.utils.helpers import sanitize_json

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def preview_data(dataset_id: str = Query(...), rows: int = 5):
    try:
        dataset = get_dataset(dataset_id)

        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")

        path = dataset["path"]

        # 🔥 Rust metadata
        total_rows = fast_count_rows(path)
        headers = fast_get_headers(path)

        df = pd.read_csv(path)

        registry.metrics_engine.log_data_stats(
            {
                "rows": total_rows,
                "columns": len(headers),
                "missing": int(df.isnull().sum().sum()),
            }
        )

        result = {
            "columns": headers,
            "shape": (total_rows, len(headers)),
            "preview": df.head(rows).to_dict(orient="records"),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing": df.isnull().sum().to_dict(),
        }

        return sanitize_json(result)

    except Exception as e:
        logger.exception("Preview failed")
        raise HTTPException(status_code=500, detail=str(e))
