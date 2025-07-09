from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .user import User
from .patient import Patient
from .medication import Medication
from .observation import Observation
from .condition import Condition
from .record import Record
from .lab import LabValue
