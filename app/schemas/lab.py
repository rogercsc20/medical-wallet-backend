from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LabValue(BaseModel):
    type: str = Field(..., description="Type of lab (e.g., creatinine, eGFR)")
    value: float = Field(..., description="Lab value")
    unit: Optional[str] = Field(None, description="Unit of measure")
    date: Optional[datetime] = Field(None, description="Date of lab")

