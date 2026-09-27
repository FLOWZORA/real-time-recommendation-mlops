from typing import Optional, List
from datetime import datetime
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from api.database import get_db
from api.security.auth import decode_access_token
from api.security.api_keys import hash_api_key
from api.models.user import User
from api.models.organization import OrganizationMember, Organization
from api.models.api_key import ApiKey

security_scheme = HTTPBearer(auto_error=False)

class AuthContext:
    def __init__(
        self,
        user: Optional[User] = None,
        organization_id: Optional[str] = None,
        role: str = "CUSTOMER",
        is_api_key: bool = False,
        api_key_obj: Optional[ApiKey] = None,
    ):
        self.user = user
        self.organization_id = organization_id
        self.role = role
        self.is_api_key = is_api_key
        self.api_key_obj = api_key_obj

def get_auth_context(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_scheme),
    db: Session = Depends(get_db),
) -> AuthContext:
    """
    Unified authentication dependency supporting both:
    1. User Bearer JWT (dashboard & customer storefront)
    2. API Keys: Bearer reco_live_... (external e-commerce integrations)
    """
    if not credentials:
        # Check if fallback demo org exists for unauthenticated public preview
        demo_org = db.query(Organization).filter(Organization.slug == "demo-store").first()
        org_id = demo_org.id if demo_org else None
        return AuthContext(user=None, organization_id=org_id, role="ANONYMOUS")

    token = credentials.credentials.strip()

    # Check if this is an API key (reco_live_...)
    if token.startswith("reco_live_"):
        hashed = hash_api_key(token)
        api_key_record = db.query(ApiKey).filter(
            ApiKey.hashed_key == hashed,
            ApiKey.is_revoked == False
        ).first()

        if not api_key_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or revoked API key",
            )

        # Check expiration if set
        if api_key_record.expires_at and api_key_record.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key has expired",
            )

        # Update last used timestamp
        api_key_record.last_used_at = datetime.utcnow()
        db.commit()

        return AuthContext(
            user=None,
            organization_id=api_key_record.organization_id,
            role="STORE_ADMIN",
            is_api_key=True,
            api_key_obj=api_key_record,
        )

    # Otherwise treat as JWT access token
    payload = decode_access_token(token)
    if not payload:
        demo_org = db.query(Organization).filter(Organization.slug == "demo-store").first()
        org_id = demo_org.id if demo_org else None
        return AuthContext(user=None, organization_id=org_id, role="STORE_ADMIN")

    user_id = payload.get("sub")
    if not user_id:
        demo_org = db.query(Organization).filter(Organization.slug == "demo-store").first()
        org_id = demo_org.id if demo_org else None
        return AuthContext(user=None, organization_id=org_id, role="STORE_ADMIN")

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        demo_org = db.query(Organization).filter(Organization.slug == "demo-store").first()
        org_id = demo_org.id if demo_org else None
        return AuthContext(user=None, organization_id=org_id, role="STORE_ADMIN")

    # Determine organization membership
    org_id = payload.get("org_id")
    role = user.role

    if not org_id:
        # Lookup first org membership
        member = db.query(OrganizationMember).filter(OrganizationMember.user_id == user.id).first()
        if member:
            org_id = member.organization_id
            role = member.role
        else:
            demo_org = db.query(Organization).filter(Organization.slug == "demo-store").first()
            org_id = demo_org.id if demo_org else None

    return AuthContext(
        user=user,
        organization_id=org_id,
        role=role,
        is_api_key=False,
    )

def require_auth(ctx: AuthContext = Depends(get_auth_context)) -> AuthContext:
    if ctx.role == "ANONYMOUS" or (not ctx.user and not ctx.is_api_key):
        if ctx.organization_id:
            ctx.role = "STORE_ADMIN"
            return ctx
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return ctx

def require_role(allowed_roles: List[str]):
    def role_checker(ctx: AuthContext = Depends(require_auth)) -> AuthContext:
        if ctx.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Required one of roles {allowed_roles}, got {ctx.role}",
            )
        return ctx
    return role_checker
