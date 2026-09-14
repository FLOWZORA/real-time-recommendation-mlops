import torch
from feast import FeatureStore

store = FeatureStore(repo_path="feature_store")

def is_cold_user(features: dict) -> bool:
    """
    User is cold if Feast returns no interaction history.
    """
    return (
        features["total_views"][0] is None and
        features["total_clicks"][0] is None and
        features["total_purchases"][0] is None
    )

def get_user_features(user_id: int):
    """
    Fetch user features from Feast and return:
    - feature tensor
    - cold-start flag
    """
    try:
        features = store.get_online_features(
            features=[
                "user_features:total_views",
                "user_features:total_clicks",
                "user_features:total_purchases",
            ],
            entity_rows=[{"user_id": user_id}],
        ).to_dict()

        cold = is_cold_user(features)

        vec = [
            features["total_views"][0] or 0,
            features["total_clicks"][0] or 0,
            features["total_purchases"][0] or 0,
            0.0, 0.0, 0.0, 0.0, 0.0
        ]
        return torch.tensor([vec], dtype=torch.float32), cold
    except Exception as e:
        # Fallback to cold start if feature store lookup encounters an issue
        default_vec = [0.0] * 8
        return torch.tensor([default_vec], dtype=torch.float32), True


