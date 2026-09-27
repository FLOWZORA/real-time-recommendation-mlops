import secrets
import hashlib
from typing import Tuple

def generate_api_key(prefix: str = "reco_live_") -> Tuple[str, str, str]:
    """
    Generates a high-entropy secret API key.
    Returns:
    - full_key: e.g. "reco_live_a1b2c3d4e5f6..." (shown only ONCE to user)
    - key_prefix: e.g. "reco_live_a1b2" (for UI display & quick lookup)
    - hashed_key: SHA-256 hex digest (stored in database)
    """
    raw_secret = secrets.token_hex(24)
    full_key = f"{prefix}{raw_secret}"
    key_prefix = full_key[:12]
    hashed_key = hash_api_key(full_key)
    return full_key, key_prefix, hashed_key

def hash_api_key(secret_key: str) -> str:
    """Computes SHA-256 hash of API key."""
    return hashlib.sha256(secret_key.encode("utf-8")).hexdigest()
