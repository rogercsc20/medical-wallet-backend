import uuid
from datetime import datetime
from sqlalchemy import (
    Column, Date, String, ForeignKey, DateTime, JSON
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    # FHIR-compliant fields
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(16), nullable=True)
    phone: Mapped[str] = mapped_column(String(32), nullable=True)
    address: Mapped[str] = mapped_column(String(256), nullable=True)
    fhir_resource: Mapped[dict] = mapped_column(JSONB, nullable=True)  # Store FHIR Patient resource as JSON

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="patient_profile")
    records = relationship("Record", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(id={self.id}, user_id={self.user_id}, name={self.first_name} {self.last_name})>"

