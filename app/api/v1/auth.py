from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    user = UserService.create_user(
        db,
        user_create.email,
        user_create.password,
        user_create.full_name,
        user_create.role
    )
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        last_login=user.last_login
    )


@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = UserService.authenticate(db, data["email"], data["password"])
    if not user:
        logger.warning("Login failed for email: %s", data["email"])
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = UserService.generate_token(user)
    logger.info("User logged in: %s", data["email"])
    return {"access_token": token, "token_type": "bearer"}

