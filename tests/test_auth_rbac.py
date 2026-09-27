import pytest
from api.security.auth import get_password_hash, verify_password, create_access_token, decode_access_token
from api.security.api_keys import generate_api_key, hash_api_key

def test_password_hashing():
    raw = "SecureP@ssw0rd123"
    hashed = get_password_hash(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_jwt_token_flow():
    payload = {"sub": "user_123", "role": "STORE_ADMIN", "org_id": "org_456"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user_123"
    assert decoded["role"] == "STORE_ADMIN"
    assert decoded["org_id"] == "org_456"

def test_api_key_generation_and_hashing():
    full_key, prefix, hashed = generate_api_key()
    assert full_key.startswith("reco_live_")
    assert prefix == full_key[:12]
    assert hashed == hash_api_key(full_key)
    # Different keys have different hashes
    _, _, hashed_2 = generate_api_key()
    assert hashed != hashed_2
