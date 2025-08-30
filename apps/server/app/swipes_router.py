from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .db import get_db
from .models import Swipe

router = APIRouter(prefix="/swipes", tags=["swipes"])


@router.post("/")
def record_swipe(user_id: str, track_id: int, liked: bool, db: Session = Depends(get_db)):
    new_swipe = Swipe(user_id=user_id, track_id=track_id, liked=liked)
    db.add(new_swipe)
    db.commit()
    db.refresh(new_swipe)
    return {"id": new_swipe.id, "message": "Swipe recorded"}
