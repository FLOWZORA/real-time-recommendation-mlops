import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch

import numpy as np
from retrieval.two_tower import TwoTower
from features.catalog_data import get_item_feature_vector, get_item_metadata, CAT_NAME_TO_INDEX
from retrieval.embed_items import generate_embeddings
from mlflow_config import *

EPOCHS = 20
LR = 0.005

def train():
    model = TwoTower()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()

    # Build genuine item feature vectors
    item_vecs = np.array([get_item_feature_vector(i) for i in range(500)], dtype=np.float32)

    # Build category interaction training dataset
    X_u, X_i, Y = [], [], []
    for _ in range(400):
        for cat_idx in range(6):
            # User profile with preference for cat_idx
            u = np.zeros(8, dtype=np.float32)
            u[cat_idx] = 1.0
            u[6] = np.random.uniform(0.5, 0.9)  # price tier
            u[7] = np.random.uniform(0.8, 1.0)  # rating preference

            # Positive items matching cat_idx
            matching = [i for i in range(500) if CAT_NAME_TO_INDEX.get(get_item_metadata(i).get("category")) == cat_idx]
            pos_id = np.random.choice(matching)
            X_u.append(u)
            X_i.append(item_vecs[pos_id])
            Y.append(1.0)

            # Negative items from other categories
            non_matching = [i for i in range(500) if CAT_NAME_TO_INDEX.get(get_item_metadata(i).get("category")) != cat_idx]
            neg_id = np.random.choice(non_matching)
            X_u.append(u)
            X_i.append(item_vecs[neg_id])
            Y.append(0.0)

    X_u = torch.tensor(np.array(X_u), dtype=torch.float32)
    X_i = torch.tensor(np.array(X_i), dtype=torch.float32)
    Y = torch.tensor(np.array(Y), dtype=torch.float32)

    for epoch in range(EPOCHS):
        optimizer.zero_grad()
        preds = model(X_u, X_i)
        loss = loss_fn(preds, Y)
        loss.backward()
        optimizer.step()

    return model, loss.item()

if __name__ == "__main__":
    model, final_loss = train()
    print(f"[OK] Training complete with final loss: {final_loss:.4f}")

    # Save local checkpoint
    torch.save(model.state_dict(), repo_root / "two_tower.pt")
    torch.save(model.state_dict(), repo_root / "retrieval" / "two_tower.pt")
    print("[OK] Saved local weights to two_tower.pt")

    # Generate item embeddings with updated weights
    generate_embeddings()

    try:
        with mlflow.start_run(run_name="two_tower_training"):
            mlflow.log_param("epochs", EPOCHS)
            mlflow.log_param("lr", LR)
            mlflow.log_param("embedding_dim", 8)
            mlflow.log_metric("final_loss", final_loss)

            mlflow.pytorch.log_model(
                model,
                artifact_path="model",
                registered_model_name="TwoTowerRecommender",
            )
            print("[OK] Model successfully registered to MLflow")

            # Promote to Production stage
            from mlflow.tracking import MlflowClient
            client = MlflowClient()
            for m in client.search_model_versions("name='TwoTowerRecommender'"):
                client.transition_model_version_stage(
                    name="TwoTowerRecommender",
                    version=m.version,
                    stage="Production"
                )
    except Exception as e:
        print(f"[WARN] MLflow logging note: {e}")


