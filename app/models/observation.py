from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models import Base

class Observation(Base):
    __tablename__ = "observations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    resource_type = Column(String(32), default="Observation", nullable=False)
    status = Column(String(32), nullable=False)
    category = Column(JSON, nullable=True)
    code = Column(JSON, nullable=False)
    subject = Column(JSON, nullable=False)
    effective_datetime = Column(DateTime, nullable=True)
    value_quantity = Column(JSON, nullable=True)
    interpretation = Column(JSON, nullable=True)

