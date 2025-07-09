from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal
from datetime import datetime

class CodeableConcept(BaseModel):
    coding: List[Dict[str, str]] = Field(..., description="List of codings (system, code, display)")
    text: Optional[str] = Field(None, description="Human-readable text")

class Reference(BaseModel):
    reference: str = Field(..., description="FHIR resource reference (e.g., Patient/123)")

class ConditionCreate(BaseModel):
    resourceType: Literal["Condition"] = Field("Condition", description="FHIR resource type")
    clinicalStatus: CodeableConcept = Field(..., description="Clinical status (e.g., active, remission)")
    verificationStatus: CodeableConcept = Field(..., description="Verification status (e.g., confirmed)")
    category: Optional[List[CodeableConcept]] = Field(None, description="Condition category (e.g., problem-list-item)")
    severity: Optional[CodeableConcept] = Field(None, description="Severity of the condition")
    code: CodeableConcept = Field(..., description="Condition code (e.g., SNOMED, ICD-10)")
    subject: Reference = Field(..., description="Subject of the condition (Patient reference)")
    onsetDateTime: Optional[datetime] = Field(None, description="Onset date/time")
    abatementDateTime: Optional[datetime] = Field(None, description="Abatement date/time")

class ConditionUpdate(BaseModel):
    clinicalStatus: Optional[CodeableConcept] = None
    verificationStatus: Optional[CodeableConcept] = None
    category: Optional[List[CodeableConcept]] = None
    severity: Optional[CodeableConcept] = None
    code: Optional[CodeableConcept] = None
    subject: Optional[Reference] = None
    onsetDateTime: Optional[datetime] = None
    abatementDateTime: Optional[datetime] = None

class ConditionResponse(ConditionCreate):
    id: str = Field(..., description="FHIR resource ID")

