from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.event import UserEvent
from api.models.product import Product
from api.schemas.event import EventCreate, BatchEventsRequest, EventResponse
from api.security.permissions import get_auth_context, AuthContext
from streaming.reward import get_reward
from streaming.consumer import process_event
from streaming.producer import LOCAL_EVENT_QUEUE, get_producer

router = APIRouter(prefix="/v1/events", tags=["Events"])

# Map event names to internal actions
ACTION_MAP = {
    "product_view": "view",
    "view": "view",
    "product_click": "click",
    "click": "click",
    "add_to_cart": "click",
    "purchase": "purchase",
    "wishlist": "click",
}

def _dispatch_event(event_dict: dict):
    # Try sending to Kafka if running, else into local queue
    producer = get_producer()
    if producer:
        try:
            producer.send("events", event_dict)
        except Exception:
            LOCAL_EVENT_QUEUE.put(event_dict)
    else:
        LOCAL_EVENT_QUEUE.put(event_dict)

    # Process stream event in real-time (Feast update + online learning)
    try:
        process_event(event_dict)
    except Exception as e:
        print(f"[WARN] Error in event stream processing: {e}")

@router.post("", response_model=EventResponse)
def ingest_event(
    req: EventCreate,
    background_tasks: BackgroundTasks,
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    action_type = ACTION_MAP.get(req.event_type, "view")
    reward = get_reward(action_type)

    # 1. Record event in PostgreSQL
    event = UserEvent(
        organization_id=ctx.organization_id or "demo-store",
        user_id=req.user_id,
        item_id_numeric=req.item_id,
        event_type=req.event_type,
        propensity=req.propensity or 0.1,
        reward=reward,
        event_metadata=req.metadata or {},
        created_at=datetime.utcnow(),
    )
    db.add(event)

    # 2. Update product popularity
    db.query(Product).filter(
        Product.organization_id == event.organization_id,
        Product.item_id_numeric == req.item_id
    ).update({Product.popularity_score: Product.popularity_score + int(reward * 10) + 1})

    db.commit()
    db.refresh(event)

    # 3. Stream processing in background
    stream_payload = {
        "user_id": int(req.user_id) if req.user_id.isdigit() else (abs(hash(req.user_id)) % 1000),
        "item_id": req.item_id,
        "action": action_type,
        "propensity": req.propensity or 0.1,
        "timestamp": datetime.utcnow().isoformat(),
    }
    background_tasks.add_task(_dispatch_event, stream_payload)

    return event

@router.post("/batch", response_model=List[EventResponse])
def ingest_batch_events(
    req: BatchEventsRequest,
    background_tasks: BackgroundTasks,
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    created_events = []
    org_id = ctx.organization_id or "demo-store"

    for ev_data in req.events:
        action_type = ACTION_MAP.get(ev_data.event_type, "view")
        reward = get_reward(action_type)

        event = UserEvent(
            organization_id=org_id,
            user_id=ev_data.user_id,
            item_id_numeric=ev_data.item_id,
            event_type=ev_data.event_type,
            propensity=ev_data.propensity or 0.1,
            reward=reward,
            event_metadata=ev_data.metadata or {},
            created_at=datetime.utcnow(),
        )
        db.add(event)
        created_events.append(event)

        stream_payload = {
            "user_id": int(ev_data.user_id) if ev_data.user_id.isdigit() else (abs(hash(ev_data.user_id)) % 1000),
            "item_id": ev_data.item_id,
            "action": action_type,
            "propensity": ev_data.propensity or 0.1,
            "timestamp": datetime.utcnow().isoformat(),
        }
        background_tasks.add_task(_dispatch_event, stream_payload)

    db.commit()
    for ev in created_events:
        db.refresh(ev)

    return created_events

@router.get("", response_model=List[EventResponse])
def list_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    ctx: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
):
    query = db.query(UserEvent)
    if ctx.organization_id:
        query = query.filter(UserEvent.organization_id == ctx.organization_id)
    if user_id:
        query = query.filter(UserEvent.user_id == user_id)
    if event_type:
        query = query.filter(UserEvent.event_type == event_type)

    return query.order_by(UserEvent.created_at.desc()).limit(limit).all()
