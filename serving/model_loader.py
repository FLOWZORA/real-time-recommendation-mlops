from pathlib import Path
import torch
import mlflow.pytorch
from mlflow_config import *
from retrieval.two_tower import TwoTower

MODEL_NAME = "TwoTowerRecommender"
MODEL_STAGE = "Production"   # Change to "Staging" if needed

print("[INFO] Loading model...")

model = None
repo_root = Path(__file__).resolve().parent.parent

# 1. Attempt loading from MLflow registry
try:
    model = mlflow.pytorch.load_model(
        f"models:/{MODEL_NAME}/{MODEL_STAGE}"
    )
    print(f"[OK] Model loaded from MLflow registry [{MODEL_NAME}:{MODEL_STAGE}]")
except Exception as e:
    print(f"[WARN] Could not load from MLflow registry ({e}). Trying local fallbacks...")

# 2. Fallback: try direct artifact path in mlruns
if model is None:
    mlruns_artifact = repo_root / "mlruns" / "1" / "models" / "m-1efc692479f24378bd28586c8c668fb0" / "artifacts"
    if mlruns_artifact.exists():
        try:
            model = mlflow.pytorch.load_model(mlruns_artifact.as_posix())
            print(f"[OK] Model loaded from MLflow artifact directory: {mlruns_artifact}")
        except Exception as e:
            print(f"[WARN] Could not load from artifact path: {e}")

# 3. Fallback: load PyTorch checkpoint directly
if model is None:
    for pt_candidate in [repo_root / "two_tower.pt", repo_root / "retrieval" / "two_tower.pt"]:
        if pt_candidate.exists():
            try:
                model = TwoTower()
                state = torch.load(pt_candidate, map_location="cpu")
                if isinstance(state, dict):
                    model.load_state_dict(state)
                else:
                    model = state
                print(f"[OK] Model loaded from PyTorch checkpoint: {pt_candidate}")
                break
            except Exception as e:
                print(f"[WARN] Could not load {pt_candidate}: {e}")

if model is None:
    print("[WARN] Checkpoint not found, initializing fresh TwoTower model")
    model = TwoTower()

model.eval()

