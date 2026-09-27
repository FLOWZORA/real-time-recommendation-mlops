from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class ApiKeyCreate(BaseModel):
    name: str
    scopes: Optional[List[str]] = ["read:recommendations", "write:events", "read:products"]

class ApiKeyResponse(BaseModel):
    id: str
    name: str
    key_prefix: str
    scopes: List[str]
    last_used_at: Optional[datetime] = None
    is_revoked: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ApiKeyCreatedResponse(ApiKeyResponse):
    secret_key: str  # Plaintext key returned only once upon creation
