from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models import Base

class Medication(Base):
    __tablename__ = "medications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    resource_type = Column(String(32), default="Medication", nullable=False)
    code = Column(JSON, nullable=False)  # CodeableConcept dict
    status = Column(String(32), default="active", nullable=True)
    manufacturer = Column(JSON, nullable=True)  # Reference dict

