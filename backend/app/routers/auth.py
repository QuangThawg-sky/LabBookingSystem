
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.security.password import verify_password
from app.security.jwt import create_access_token
from app.security.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.scalar(
        select(User).where(User.email == request.email)
    )

    if user is None or not verify_password(
        request.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/staff-only")
def staff_only(
    current_user: User = Depends(require_roles("staff"))
):
    return {
        "message": "Ban co quyen truy cap chuc nang nhan vien",
        "user": current_user.full_name,
        "role": current_user.role
    }
