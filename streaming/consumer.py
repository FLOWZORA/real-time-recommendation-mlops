import sys
import json
from pathlib import Path
from datetime import datetime
from queue import Empty
import torch
import pandas as pd
from jsonschema import validate

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# -----------------------------
# Project imports
# -----------------------------
from serving.model_loader import model
from serving.user_features import get_user_features
from model.online_update import online_update
from streaming.reward import get_reward
from evaluation.logged_data import log_event
from monitoring.drift_stats import log_reward
from streaming.producer import LOCAL_EVENT_QUEUE

# -----------------------------
# Load JSON schema
# -----------------------------
schema_path = Path(__file__).parent / "schema.json"
with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

# -----------------------------
# Feast Feature Store
# -----------------------------
store = None
try:
    from feast import FeatureStore
    store = FeatureStore(repo_path=(repo_root / "feature_store").as_posix())
except Exception as e:
    print(f"[WARN] Feature store initialization in consumer: {e}")

def get_consumer(bootstrap_servers="localhost:9092"):
    try:
        from kafka import KafkaConsumer
        consumer = KafkaConsumer(
            "events",
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True,
            consumer_timeout_ms=2000,
        )
        print("[OK] Connected to Kafka consumer")
        return consumer
    except Exception as e:
        print(f"[INFO] Kafka consumer unavailable ({e}). Using local in-memory queue fallback.")
        return None

def process_event(event: dict):
    """
    Process a single recommendation interaction event:
    1. Schema validation
    2. Logging for counterfactual evaluation (IPS/DR)
    3. Update Feast online features
    4. Online learning update
    5. Monitoring drift stat update
    """
    validate(instance=event, schema=schema)

    user_id = event["user_id"]
    item_id = event["item_id"]
    action = event["action"]
    propensity = event.get("propensity", 0.1)

    # 1. Log event for IPS / DR
    log_event(event)

    # 2. Update Feast online features
    if store is not None:
        try:
            feature_df = pd.DataFrame([{
                "user_id": user_id,
                "total_views": 1 if action == "view" else 0,
                "total_clicks": 1 if action == "click" else 0,
                "total_purchases": 1 if action == "purchase" else 0,
                "event_timestamp": datetime.utcnow(),
            }])

            store.write_to_online_store(
                feature_view_name="user_features",
                df=feature_df,
            )
        except Exception as e:
            pass

    # 3. Online learning update
    reward = get_reward(action)

    if reward > 0:
        # Correctly unpack tuple: (tensor, is_cold)
        user_features_tensor, is_cold = get_user_features(user_id)

        # Item features
        item_features = torch.rand(1, 8)

        loss = online_update(
            model=model,
            user_features=user_features_tensor,
            item_features=item_features,
            label=reward,
        )

        print(
            f"[OK] Online update | user={user_id} "
            f"item={item_id} action={action} loss={loss:.4f}"
        )

    # 4. Drift monitoring stat update
    log_reward(reward)

def consume_events(max_messages=None, consumer=None):
    if consumer is None:
        consumer = get_consumer()

    print(f"[INFO] Consuming events (max: {max_messages or 'infinite'})...")
    count = 0

    if consumer:
        for msg in consumer:
            event = msg.value
            process_event(event)
            count += 1
            if max_messages and count >= max_messages:
                break
    else:
        # Drain local in-memory event queue
        while max_messages is None or count < max_messages:
            try:
                event = LOCAL_EVENT_QUEUE.get(timeout=1)
                process_event(event)
                count += 1
            except Empty:
                break

    print(f"[OK] Consumed {count} events successfully")
    return count

if __name__ == "__main__":
    consume_events(max_messages=5)

