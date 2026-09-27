from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.api_key import ApiKey
from api.schemas.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyCreatedResponse
from api.security.api_keys import generate_api_key
from api.security.permissions import require_role, AuthContext

router = APIRouter(prefix="/v1/api-keys", tags=["API Keys"])

@router.get("", response_model=List[ApiKeyResponse])
def list_api_keys(
    ctx: AuthContext = Depends(require_role(["STORE_ADMIN"])),
    db: Session = Depends(get_db),
):
    org_id = ctx.organization_id or "demo-store"
    keys = db.query(ApiKey).filter(ApiKey.organization_id == org_id).order_by(ApiKey.created_at.desc()).all()
    return keys

@router.post("", response_model=ApiKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
def create_api_key(
    req: ApiKeyCreate,
    ctx: AuthContext = Depends(require_role(["STORE_ADMIN"])),
    db: Session = Depends(get_db),
):
    org_id = ctx.organization_id or "demo-store"
    secret_key, prefix, hashed = generate_api_key()

    key_record = ApiKey(
        organization_id=org_id,
        name=req.name,
        key_prefix=prefix,
        hashed_key=hashed,
        scopes=req.scopes or ["read:recommendations", "write:events"],
    )
    db.add(key_record)
    db.commit()
    db.refresh(key_record)

    return ApiKeyCreatedResponse(
        id=key_record.id,
        name=key_record.name,
        key_prefix=key_record.key_prefix,
        scopes=key_record.scopes,
        is_revoked=key_record.is_revoked,
        created_at=key_record.created_at,
        secret_key=secret_key,
    )

@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: str,
    ctx: AuthContext = Depends(require_role(["STORE_ADMIN"])),
    db: Session = Depends(get_db),
):
    org_id = ctx.organization_id or "demo-store"
    key_record = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.organization_id == org_id
    ).first()
    if not key_record:
        raise HTTPException(status_code=404, detail="API key not found")

    key_record.is_revoked = True
    db.commit()
    return None
