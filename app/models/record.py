import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class RecordType(str, Enum):
    LAB = "lab"
    MEDICATION = "medication"
    NOTE = "note"
    SUMMARY = "summary"
    OTHER = "other"

class Record(Base):
    __tablename__ = "records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    record_type: Mapped[RecordType] = mapped_column(String(32), nullable=False)
    source: Mapped[str] = mapped_column(String(128), nullable=True)  # EHR, lab, provider, patient, etc.
    fhir_resource: Mapped[dict] = mapped_column(JSONB, nullable=False)  # Store the full FHIR resource
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="records")

    def __repr__(self):
        return f"<Record(id={self.id}, patient_id={self.patient_id}, type={self.record_type})>"

