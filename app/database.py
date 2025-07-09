import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings

# Configure logging for database operations
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine with connection pooling and pre-ping for stale connection cleanup
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,   
    )
    logger.info("SQLAlchemy engine created successfully.")
except SQLAlchemyError as e:
    logger.error(f"Failed to create SQLAlchemy engine: {e}")
    raise

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

def get_db():
    """
    Dependency that provides a SQLAlchemy session.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")

