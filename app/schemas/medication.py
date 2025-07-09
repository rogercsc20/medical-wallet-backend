from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal

class CodeableConcept(BaseModel):
    coding: List[Dict[str, str]] = Field(..., description="List of codings (system, code, display)")
    text: Optional[str] = Field(None, description="Human-readable text")

class Reference(BaseModel):
    reference: str = Field(..., description="FHIR resource reference (e.g., Patient/123)")

class MedicationCreate(BaseModel):
    resourceType: Literal["Medication"] = Field("Medication", description="FHIR resource type")
    code: CodeableConcept = Field(..., description="Medication code (RxNorm, ATC, etc.)")
    status: Optional[Literal["active", "inactive", "entered-in-error"]] = Field("active", description="Medication status")
    manufacturer: Optional[Reference] = Field(None, description="Manufacturer reference")

class MedicationUpdate(BaseModel):
    code: Optional[CodeableConcept] = None
    status: Optional[Literal["active", "inactive", "entered-in-error"]] = None
    manufacturer: Optional[Reference] = None

class MedicationResponse(MedicationCreate):
    id: str = Field(..., description="FHIR resource ID")

