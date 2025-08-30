from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .db import get_db
from .models import Track
from .s3 import get_s3_client

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("/", response_model=List[dict])
def get_tracks(db: Session = Depends(get_db)):
    tracks = db.query(Track).filter(Track.is_active == True).all()
    return [{"id": t.id, "title": t.title, "artist": t.artist, "genre": t.genre} for t in tracks]


@router.get("/{track_id}")
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id, Track.is_active == True).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"id": track.id, "title": track.title, "artist": track.artist, "genre": track.genre, "s3_key": track.s3_key}


@router.post("/")
def create_track(title: str, artist: str, genre: str = None, s3_key: str = None, db: Session = Depends(get_db)):
    new_track = Track(title=title, artist=artist, genre=genre, s3_key=s3_key)
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return {"id": new_track.id, "message": "Track created"}
