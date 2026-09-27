from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from api.database import get_db
from api.models.user import User
from api.models.organization import Organization, OrganizationMember
from api.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserResponse
from api.security.auth import verify_password, get_password_hash, create_access_token
from api.security.permissions import require_auth, AuthContext

router = APIRouter(prefix="/v1/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Create Organization if specified or use demo org
    org_slug = req.organization_name.lower().replace(" ", "-") + "-" + str(uuid.uuid4())[:8]
    org = Organization(
        name=req.organization_name,
        slug=org_slug,
        plan="free",
    )
    db.add(org)
    db.flush()

    # Create User
    user = User(
        email=req.email,
        hashed_password=get_password_hash(req.password),
        full_name=req.full_name,
        role=req.role or "STORE_ADMIN",
    )
    db.add(user)
    db.flush()

    # Link Membership
    member = OrganizationMember(
        organization_id=org.id,
        user_id=user.id,
        role=user.role,
    )
    db.add(member)
    db.commit()

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role, "org_id": org.id})

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        role=user.role,
        organization_id=org.id,
    )

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Get org membership
    member = db.query(OrganizationMember).filter(OrganizationMember.user_id == user.id).first()
    org_id = member.organization_id if member else None

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role, "org_id": org_id})

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        role=user.role,
        organization_id=org_id,
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(ctx: AuthContext = Depends(require_auth)):
    if not ctx.user:
        raise HTTPException(status_code=400, detail="Authenticated via API Key, not user session")
    return UserResponse(
        id=ctx.user.id,
        email=ctx.user.email,
        full_name=ctx.user.full_name,
        role=ctx.role,
        is_active=ctx.user.is_active,
        organization_id=ctx.organization_id,
    )
