import sys
from pathlib import Path
import numpy as np

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from vector_db.milvus import insert_embeddings

def load_items():
    npy_path = None
    for p in [repo_root / "item_embeddings.npy", repo_root / "retrieval" / "item_embeddings.npy"]:
        if p.exists():
            npy_path = p
            break

    if npy_path is None:
        raise FileNotFoundError("Could not find item_embeddings.npy in root or retrieval/")

    embeddings = np.load(npy_path)
    insert_embeddings(embeddings)
    print(f"[OK] Item embeddings loaded ({len(embeddings)} items) from {npy_path.name}")

if __name__ == "__main__":
    load_items()

