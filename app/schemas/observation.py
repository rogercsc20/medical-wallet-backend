from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal
from datetime import datetime

class CodeableConcept(BaseModel):
    coding: List[Dict[str, str]] = Field(..., description="List of codings (system, code, display)")
    text: Optional[str] = Field(None, description="Human-readable text")

class Quantity(BaseModel):
    value: float = Field(..., description="Numerical value")
    unit: Optional[str] = Field(None, description="Unit of measure")
    system: Optional[str] = Field(None, description="Unit system URI")
    code: Optional[str] = Field(None, description="Unit code")

class Reference(BaseModel):
    reference: str = Field(..., description="FHIR resource reference (e.g., Patient/123)")

class ObservationCreate(BaseModel):
    resourceType: Literal["Observation"] = Field("Observation", description="FHIR resource type")
    status: Literal[
        "registered", "preliminary", "final", "amended", "corrected", "cancelled", "entered-in-error", "unknown"
    ] = Field(..., description="Observation status")
    category: Optional[List[CodeableConcept]] = Field(None, description="Observation category (e.g., laboratory)")
    code: CodeableConcept = Field(..., description="Observation code (e.g., LOINC)")
    subject: Reference = Field(..., description="Subject of the observation (Patient reference)")
    effectiveDateTime: Optional[datetime] = Field(None, description="Time of the observation")
    valueQuantity: Optional[Quantity] = Field(None, description="Quantity value")
    interpretation: Optional[List[CodeableConcept]] = Field(None, description="Interpretation of the result")

class ObservationUpdate(BaseModel):
    status: Optional[
        Literal[
            "registered", "preliminary", "final", "amended", "corrected", "cancelled", "entered-in-error", "unknown"
        ]
    ] = None
    category: Optional[List[CodeableConcept]] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    effectiveDateTime: Optional[datetime] = None
    valueQuantity: Optional[Quantity] = None
    interpretation: Optional[List[CodeableConcept]] = None

class ObservationResponse(ObservationCreate):
    id: str = Field(..., description="FHIR resource ID")

