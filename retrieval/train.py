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

from retrieval.two_tower import TwoTower
from mlflow_config import *

EPOCHS = 5
LR = 0.001

def train():
    model = TwoTower()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()

    # Dummy training loop (replace with real data later)
    for epoch in range(EPOCHS):
        user = torch.rand(32, 8)
        item = torch.rand(32, 8)
        labels = torch.randint(0, 2, (32,)).float()

        preds = model(user, item)
        loss = loss_fn(preds, labels)

        optimizer.zero_grad()
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
    except Exception as e:
        print(f"[WARN] Could not log to MLflow ({e}). Local weights saved successfully.")

