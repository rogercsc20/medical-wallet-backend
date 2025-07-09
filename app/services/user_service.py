from app.models.user import User
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.core.jwt import create_access_token
import logging

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if user and bcrypt.verify(password, user.password_hash):
            logger.info("User authenticated: %s", email)
            return user
        logger.warning("Authentication failed for email: %s", email)
        return None

    @staticmethod
    def create_user(db: Session, email: str, password: str, full_name: str, role: str):
        hashed_pw = bcrypt.hash(password)
        user = User(email=email, password_hash=hashed_pw, full_name=full_name, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("User created: %s", email)
        return user

    @staticmethod
    def generate_token(user: User):
        token = create_access_token({"sub": str(user.id), "role": user.role})
        logger.info("JWT token generated for user_id=%s", user.id)
        return token

