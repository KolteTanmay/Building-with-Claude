from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Order
from schemas import OrderCreate, OrderOut, MessageResponse
from utils.notifications import notify_owner_new_order, notify_customer_received, whatsapp_owner_new_order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def submit_order(payload: OrderCreate, db: Session = Depends(get_db)):
    """
    Public endpoint — called from the frontend order form.
    Creates an order and sends notifications to owner and customer.
    """
    order = Order(**payload.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)

    # Fire notifications (non-blocking — errors are logged, not raised)
    try:
        notify_owner_new_order(order)
        notify_customer_received(order)
        whatsapp_owner_new_order(order)
    except Exception as e:
        print(f"[NOTIFICATION ERROR] {e}")

    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Public endpoint — lets a customer check their order status by ID.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
