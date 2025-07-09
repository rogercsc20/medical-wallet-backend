from datetime import datetime, timedelta
import jwt
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.info("JWT access token created for user_id=%s", data.get("sub"))
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.info("JWT access token decoded for user_id=%s", payload.get("sub"))
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        raise
    except jwt.PyJWTError as e:
        logger.warning("JWT decode error: %s", str(e))
        raise

