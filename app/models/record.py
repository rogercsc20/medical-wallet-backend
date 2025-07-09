from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models import Base

class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    resource_type = Column(String(32), default="Encounter", nullable=False)
    status = Column(String(32), nullable=False)
    class_ = Column("class", JSON, nullable=False)
    subject = Column(JSON, nullable=False)
    period = Column(JSON, nullable=True)

