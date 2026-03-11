from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import GalleryItem
from schemas import GalleryItemCreate, GalleryItemUpdate, GalleryItemOut
from utils.auth import get_current_admin

router = APIRouter(prefix="/gallery", tags=["Gallery"])


@router.get("/", response_model=List[GalleryItemOut])
def get_gallery(db: Session = Depends(get_db)):
    """Public — returns all visible gallery items sorted by sort_order."""
    return (
        db.query(GalleryItem)
        .filter(GalleryItem.is_visible == True)
        .order_by(GalleryItem.sort_order, GalleryItem.id)
        .all()
    )


@router.post("/", response_model=GalleryItemOut, status_code=status.HTTP_201_CREATED)
def add_gallery_item(
    payload: GalleryItemCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — add a new gallery item."""
    item = GalleryItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=GalleryItemOut)
def update_gallery_item(
    item_id: int,
    payload: GalleryItemUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — update a gallery item."""
    item = db.query(GalleryItem).filter(GalleryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_gallery_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — delete a gallery item."""
    item = db.query(GalleryItem).filter(GalleryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    db.delete(item)
    db.commit()
    return {"message": f"Gallery item {item_id} deleted"}
