from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ── ORDER SCHEMAS ──────────────────────────────────────────────

class OrderCreate(BaseModel):
    full_name:    str  = Field(..., min_length=2, max_length=100)
    phone:        str  = Field(..., min_length=7, max_length=20)
    email:        Optional[EmailStr] = None
    category:     str  = Field(..., min_length=1)
    budget_range: Optional[str] = None
    description:  str  = Field(..., min_length=10)


class OrderUpdate(BaseModel):
    status:      Optional[str] = None
    admin_notes: Optional[str] = None


class OrderOut(BaseModel):
    id:           int
    full_name:    str
    phone:        str
    email:        Optional[str]
    category:     str
    budget_range: Optional[str]
    description:  str
    status:       str
    admin_notes:  Optional[str]
    created_at:   datetime
    updated_at:   Optional[datetime]

    class Config:
        from_attributes = True


# ── GALLERY SCHEMAS ────────────────────────────────────────────

class GalleryItemCreate(BaseModel):
    title:       str  = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    image_url:   str  = Field(..., min_length=5)
    category:    str  = Field(..., min_length=1)
    tag_color:   Optional[str] = "blue"
    is_visible:  Optional[bool] = True
    sort_order:  Optional[int] = 0


class GalleryItemUpdate(BaseModel):
    title:       Optional[str] = None
    description: Optional[str] = None
    image_url:   Optional[str] = None
    category:    Optional[str] = None
    tag_color:   Optional[str] = None
    is_visible:  Optional[bool] = None
    sort_order:  Optional[int] = None


class GalleryItemOut(BaseModel):
    id:          int
    title:       str
    description: Optional[str]
    image_url:   str
    category:    str
    tag_color:   str
    is_visible:  bool
    sort_order:  int
    created_at:  datetime

    class Config:
        from_attributes = True


# ── AUTH SCHEMAS ───────────────────────────────────────────────

class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type:   str


# ── GENERIC ────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str
