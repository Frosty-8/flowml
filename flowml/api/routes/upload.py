from fastapi import APIRouter, UploadFile, File, HTTPException
import os , uuid
from flowml.storage.sqlite import create_dataset


router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        dataset_id = create_dataset(
            name=file.filename,
            dtype="csv",
            path=file_path
        )

        return {
            "dataset_id": dataset_id,
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))