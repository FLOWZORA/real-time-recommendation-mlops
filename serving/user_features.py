import torch
import numpy as np
from feast import FeatureStore
from features.catalog_data import get_user_persona, USER_PERSONAS

store = None
try:
    store = FeatureStore(repo_path="feature_store")
except Exception as e:
    print(f"[WARN] Feast feature store init: {e}")

def is_cold_user(features: dict, user_id: int) -> bool:
    """
    User is cold if explicitly designated or if Feast returns no interaction history.
    """
    if user_id == 999:
        return True
    if user_id in USER_PERSONAS and user_id != 999:
        return False

    return (
        features.get("total_views", [None])[0] is None and
        features.get("total_clicks", [None])[0] is None and
        features.get("total_purchases", [None])[0] is None
    )

def get_user_features(user_id: int):
    """
    Fetch user features returning:
    - feature tensor (1, 8)
    - cold-start flag (bool)
    """
    persona = get_user_persona(user_id)
    base_vec = list(persona.get("feature_vector", [0.0] * 8))

    views = persona.get("views", 0)
    clicks = persona.get("clicks", 0)
    purchases = persona.get("purchases", 0)
    cold = (user_id == 999) or (user_id not in USER_PERSONAS)

    # Attempt fetching live telemetry from Feast
    if store is not None:
        try:
            features = store.get_online_features(
                features=[
                    "user_features:total_views",
                    "user_features:total_clicks",
                    "user_features:total_purchases",
                ],
                entity_rows=[{"user_id": int(user_id)}],
            ).to_dict()

            feast_views = features.get("total_views", [None])[0]
            feast_clicks = features.get("total_clicks", [None])[0]
            feast_purchases = features.get("total_purchases", [None])[0]

            if feast_views is not None:
                views = max(views, feast_views)
            if feast_clicks is not None:
                clicks = max(clicks, feast_clicks)
            if feast_purchases is not None:
                purchases = max(purchases, feast_purchases)

            if user_id != 999 and ((feast_views is not None and feast_views > 0) or (feast_clicks is not None and feast_clicks > 0) or (feast_purchases is not None and feast_purchases > 0)):
                cold = False
        except Exception:
            pass

    # The 8-dim vector represents category affinities (0..5), price tier (6), rating preference (7)
    tensor = torch.tensor([base_vec], dtype=torch.float32)
    return tensor, cold



