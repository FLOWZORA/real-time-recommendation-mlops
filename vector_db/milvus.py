import os
import time
from pathlib import Path
import numpy as np

# Try importing pymilvus
try:
    from pymilvus import (
        connections,
        FieldSchema,
        CollectionSchema,
        DataType,
        Collection,
        utility,
    )
    PYMILVUS_AVAILABLE = True
except ImportError:
    PYMILVUS_AVAILABLE = False

COLLECTION_NAME = "item_embeddings"
VECTOR_DIM = 32   # must match Two-Tower embedding size

_milvus_connected = False
_local_embeddings = None
_local_ids = []

def init_milvus(host="127.0.0.1", port="19530", timeout=2):
    """
    Attempt to connect to Milvus server. Returns True if connected, False otherwise.
    """
    global _milvus_connected
    if not PYMILVUS_AVAILABLE:
        _milvus_connected = False
        return False

    try:
        connections.connect(
            alias="default",
            host=host,
            port=port,
            timeout=timeout
        )
        _milvus_connected = True
        print("[OK] Connected to Milvus server")
        return True
    except Exception:
        _milvus_connected = False
        return False

# Attempt quick connection on module load (non-blocking, 1 attempt)
if os.getenv("SKIP_MILVUS_CONNECT", "0") != "1":
    init_milvus(timeout=1)

if not _milvus_connected:
    print("[INFO] Milvus server not detected. Using local in-memory vector index fallback.")
    # Initialize local fallback with existing item_embeddings.npy if available
    repo_root = Path(__file__).resolve().parent.parent
    candidates = [
        repo_root / "item_embeddings.npy",
        repo_root / "retrieval" / "item_embeddings.npy"
    ]
    for p in candidates:
        if p.exists():
            try:
                _local_embeddings = np.load(p)
                _local_ids = list(range(len(_local_embeddings)))
                print(f"[OK] Loaded {len(_local_ids)} embeddings into local vector index from {p.name}")
                break
            except Exception as e:
                print(f"[WARN] Failed loading {p}: {e}")

# -----------------------------
# Create / Load Collection
# -----------------------------
def get_collection():
    if not _milvus_connected:
        return None

    if not utility.has_collection(COLLECTION_NAME):
        fields = [
            FieldSchema(
                name="item_id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=False
            ),
            FieldSchema(
                name="vector",
                dtype=DataType.FLOAT_VECTOR,
                dim=VECTOR_DIM
            ),
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Item embeddings for recommendations"
        )

        collection = Collection(
            name=COLLECTION_NAME,
            schema=schema
        )

        collection.create_index(
            field_name="vector",
            index_params={
                "index_type": "IVF_FLAT",
                "metric_type": "IP",
                "params": {"nlist": 128}
            }
        )
    else:
        collection = Collection(COLLECTION_NAME)

    collection.load()
    return collection


# -----------------------------
# INSERT ITEM EMBEDDINGS
# -----------------------------
def insert_embeddings(embeddings: np.ndarray):
    """
    embeddings: np.ndarray of shape (num_items, VECTOR_DIM)
    """
    global _local_embeddings, _local_ids
    _local_embeddings = embeddings
    _local_ids = list(range(len(embeddings)))

    if _milvus_connected:
        try:
            collection = get_collection()
            vectors = embeddings.tolist()
            collection.insert([_local_ids, vectors])
            collection.flush()
            print(f"[OK] Inserted {len(_local_ids)} item embeddings into Milvus")
            return
        except Exception as e:
            print(f"[WARN] Milvus insert failed ({e}). Stored in local vector index.")

    print(f"[OK] Stored {len(_local_ids)} item embeddings in local vector index")


# -----------------------------
# SEARCH (used by API)
# -----------------------------
def search(user_embedding, top_k=10):
    """
    ANN search returning candidate item IDs.
    user_embedding can be a 1D or 2D array / tensor.
    """
    if hasattr(user_embedding, "detach"):
        user_embedding = user_embedding.detach().cpu().numpy()
    user_vec = np.asarray(user_embedding, dtype=np.float32)

    # Flatten if 2D (1, D)
    if user_vec.ndim == 2:
        query_2d = user_vec
        query_1d = user_vec[0]
    else:
        query_2d = np.expand_dims(user_vec, axis=0)
        query_1d = user_vec

    if _milvus_connected:
        try:
            collection = get_collection()
            results = collection.search(
                data=query_2d.tolist(),
                anns_field="vector",
                param={"metric_type": "IP", "params": {"nprobe": 10}},
                limit=top_k
            )
            return [hit.id for hit in results[0]]
        except Exception as e:
            print(f"[WARN] Milvus search failed ({e}). Falling back to local index.")

    # Local fallback using Inner Product (IP) similarity
    global _local_embeddings, _local_ids
    if _local_embeddings is None or len(_local_embeddings) == 0:
        # Generate default items if index is completely empty
        return list(range(min(top_k, 50)))

    # Compute dot products: (N, D) @ (D,) -> (N,)
    scores = np.dot(_local_embeddings, query_1d)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [_local_ids[idx] for idx in top_indices]


