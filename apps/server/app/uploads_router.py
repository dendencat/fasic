from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from .db import get_db
from .models import Upload
from .s3 import get_s3_client

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/")
def upload_file(file: UploadFile = File(...), user_id: str = "user1", db: Session = Depends(get_db)):
    s3_client = get_s3_client()
    if not s3_client:
        raise HTTPException(status_code=500, detail="S3 client not available")

    # Upload to S3
    s3_key = f"uploads/{user_id}/{file.filename}"
    s3_client.put_object(Bucket="swipetune-tracks", Key=s3_key, Body=file.file.read())

    # Save to DB
    new_upload = Upload(user_id=user_id, file_name=file.filename, s3_key=s3_key)
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    return {"id": new_upload.id, "message": "File uploaded", "s3_key": s3_key}
