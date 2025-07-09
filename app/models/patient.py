from sqlalchemy import Column, String, Date, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    resource_type = Column(String(32), default="Patient", nullable=False)
    name = Column(JSON, nullable=False)  # List of HumanName dicts
    gender = Column(String(16), nullable=False)
    birth_date = Column(Date, nullable=False)
    telecom = Column(JSON, nullable=True)

