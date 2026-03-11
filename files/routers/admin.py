from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Order
from schemas import AdminLogin, Token, OrderOut, OrderUpdate, MessageResponse
from utils.auth import authenticate_admin, create_access_token, get_current_admin
from utils.notifications import notify_customer_status_update

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login", response_model=Token)
def login(payload: AdminLogin):
    """Admin login — returns a JWT token."""
    if not authenticate_admin(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": payload.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/orders", response_model=List[OrderOut])
def list_orders(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — list all orders with optional status filter."""
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    return (
        query.order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/orders/stats")
def order_stats(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — quick stats for the dashboard."""
    total     = db.query(Order).count()
    pending   = db.query(Order).filter(Order.status == "pending").count()
    printing  = db.query(Order).filter(Order.status == "printing").count()
    delivered = db.query(Order).filter(Order.status == "delivered").count()
    cancelled = db.query(Order).filter(Order.status == "cancelled").count()

    return {
        "total":     total,
        "pending":   pending,
        "printing":  printing,
        "delivered": delivered,
        "cancelled": cancelled,
    }


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — get a single order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/orders/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — update order status and/or notes. Notifies customer by email."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    status_changed = payload.status and payload.status != order.status

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)

    # Notify customer if status changed
    if status_changed:
        try:
            notify_customer_status_update(order)
        except Exception as e:
            print(f"[NOTIFICATION ERROR] {e}")

    return order


@router.delete("/orders/{order_id}", response_model=MessageResponse)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """Admin only — delete an order."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted"}
