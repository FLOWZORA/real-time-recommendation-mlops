import sys
import json
import time
import random
import datetime
from pathlib import Path
from queue import Queue

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Shared local queue for in-memory streaming testing when Kafka is offline
LOCAL_EVENT_QUEUE = Queue()

def get_producer(bootstrap_servers="localhost:9092"):
    try:
        from kafka import KafkaProducer
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode(),
            request_timeout_ms=1000,
        )
        print("[OK] Connected to Kafka producer")
        return producer
    except Exception as e:
        print(f"[INFO] Kafka producer unavailable ({e}). Using local in-memory queue fallback.")
        return None

def generate_event(user_id=None, item_id=None, action=None):
    return {
        "user_id": user_id if user_id is not None else random.randint(1, 100),
        "item_id": item_id if item_id is not None else random.randint(1, 500),
        "action": action if action is not None else random.choice(["view", "click", "purchase"]),
        "propensity": 0.1,  # probability of showing item (baseline policy)
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }

def produce_events(count=10, interval=0.1, producer=None):
    if producer is None:
        producer = get_producer()

    print(f"[INFO] Producing {count if count else 'infinite'} events...")
    sent = 0
    while count is None or sent < count:
        event = generate_event()
        if producer:
            try:
                producer.send("events", event)
            except Exception as e:
                print(f"[WARN] Failed sending to Kafka: {e}")
                LOCAL_EVENT_QUEUE.put(event)
        else:
            LOCAL_EVENT_QUEUE.put(event)

        sent += 1
        print(f"[OK] Produced event {sent}: user={event['user_id']} item={event['item_id']} action={event['action']}")
        if interval > 0:
            time.sleep(interval)

if __name__ == "__main__":
    produce_events(count=5, interval=0.1)

