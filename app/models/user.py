import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Enum, ForeignKey, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class UserRole(str, Enum):
    PATIENT = "patient"
    PROVIDER = "provider"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint('email', name='uq_user_email'),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.PATIENT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    patient_profile = relationship("Patient", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

