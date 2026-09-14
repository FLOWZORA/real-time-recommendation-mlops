import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

import torch
import numpy as np
from retrieval.two_tower import TwoTower


def generate_embeddings(num_items=500):
    repo_root = Path(__file__).resolve().parent.parent
    
    # Locate checkpoint
    model_path = None
    for p in [repo_root / "two_tower.pt", repo_root / "retrieval" / "two_tower.pt"]:
        if p.exists():
            model_path = p
            break

    model = TwoTower()
    if model_path:
        state = torch.load(model_path, map_location="cpu")
        if isinstance(state, dict):
            model.load_state_dict(state)
        else:
            model = state
        print(f"[OK] Loaded checkpoint from {model_path}")
    else:
        print("[WARN] No checkpoint found; using initialized model weights")

    model.eval()

    # Example item features
    item_features = torch.rand(num_items, 8)

    with torch.no_grad():
        embeddings = model.item(item_features).numpy()

    # Save to both locations for compatibility
    np.save(repo_root / "item_embeddings.npy", embeddings)
    (repo_root / "retrieval").mkdir(exist_ok=True)
    np.save(repo_root / "retrieval" / "item_embeddings.npy", embeddings)

    print(f"[OK] Saved {len(embeddings)} item embeddings to item_embeddings.npy")
    return embeddings

if __name__ == "__main__":
    generate_embeddings()

