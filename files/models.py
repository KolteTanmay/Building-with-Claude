from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from database import Base
import enum


class OrderStatus(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    printing  = "printing"
    finishing = "finishing"
    shipped   = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderCategory(str, enum.Enum):
    custom_gift   = "Custom Gift"
    showpiece     = "Showpiece / Decor"
    diy_kit       = "DIY Kit"
    anime         = "Anime / Pop Culture"
    signage       = "Name Plate / Signage"
    prototype     = "Prototype / Part"
    other         = "Other"


class Order(Base):
    __tablename__ = "orders"

    id            = Column(Integer, primary_key=True, index=True)
    full_name     = Column(String(100), nullable=False)
    phone         = Column(String(20),  nullable=False)
    email         = Column(String(100), nullable=True)
    category      = Column(String(50),  nullable=False)
    budget_range  = Column(String(30),  nullable=True)
    description   = Column(Text,        nullable=False)
    status        = Column(String(20),  default=OrderStatus.pending, nullable=False)
    admin_notes   = Column(Text,        nullable=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), onupdate=func.now())


class GalleryItem(Base):
    __tablename__ = "gallery_items"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(100), nullable=False)
    description = Column(Text,        nullable=True)
    image_url   = Column(String(500), nullable=False)
    category    = Column(String(50),  nullable=False)
    tag_color   = Column(String(10),  default="blue")   # "blue" or "green"
    is_visible  = Column(Boolean,     default=True)
    sort_order  = Column(Integer,     default=0)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
