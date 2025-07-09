from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models import Base

class Condition(Base):
    __tablename__ = "conditions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    resource_type = Column(String(32), default="Condition", nullable=False)
    clinical_status = Column(JSON, nullable=False)
    verification_status = Column(JSON, nullable=False)
    category = Column(JSON, nullable=True)
    severity = Column(JSON, nullable=True)
    code = Column(JSON, nullable=False)
    subject = Column(JSON, nullable=False)
    onset_datetime = Column(DateTime, nullable=True)
    abatement_datetime = Column(DateTime, nullable=True)

