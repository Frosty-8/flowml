from fastapi import APIRouter, HTTPException, Query
from flowml.storage.sqlite import get_dataset
import pandas as pd
from flowml.utils.helpers import sanitize_json

router = APIRouter()


@router.get("/summary")
def summary_stats(dataset_id: str = Query(...)):
    dataset = get_dataset(dataset_id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    path = dataset["path"]

    df = pd.read_csv(path)

    result = df.describe().to_dict()

    return sanitize_json(result)