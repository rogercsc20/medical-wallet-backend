from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal
from datetime import datetime

class RecordCreate(BaseModel):
    resourceType: Literal["Encounter"] = Field("Encounter", description="FHIR resource type")
    status: Literal["planned", "in-progress", "finished", "cancelled"] = Field(..., description="Encounter status")
    class_: Dict[str, str] = Field(..., alias="class", description="Class of encounter (e.g., inpatient, outpatient)")
    subject: Dict[str, str] = Field(..., description="Reference to Patient")
    period: Optional[Dict[str, datetime]] = Field(None, description="Start/end time")

class RecordUpdate(BaseModel):
    status: Optional[Literal["planned", "in-progress", "finished", "cancelled"]] = None
    class_: Optional[Dict[str, str]] = Field(None, alias="class")
    period: Optional[Dict[str, datetime]] = None

class RecordResponse(RecordCreate):
    id: str = Field(..., description="FHIR resource ID")

