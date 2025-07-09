from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Literal
from datetime import date

class HumanName(BaseModel):
    family: str = Field(..., description="Family name (last name)")
    given: List[str] = Field(..., description="Given names (first and middle names)")

class ContactPoint(BaseModel):
    system: Optional[str] = Field(None, description="Contact system (e.g., phone, email)")
    value: Optional[str] = Field(None, description="Contact value")
    use: Optional[str] = Field(None, description="Use of contact point (e.g., home, work)")

class PatientCreate(BaseModel):
    resourceType: Literal["Patient"] = Field("Patient", description="FHIR resource type")
    name: List[HumanName] = Field(..., description="Patient's name(s)")
    gender: str = Field(..., description="Patient gender")
    birthDate: date = Field(..., description="Patient birth date")
    telecom: Optional[List[ContactPoint]] = Field(None, description="Contact information")

    @field_validator('gender')
    @classmethod
    def gender_must_be_valid(cls, v):
        valid_genders = {'male', 'female', 'other', 'unknown'}
        if v.lower() not in valid_genders:
            raise ValueError(f"Invalid gender: {v}. Must be one of {valid_genders}")
        return v.lower()

    @field_validator('birthDate')
    @classmethod
    def birth_date_must_be_past(cls, v):
        if v >= date.today():
            raise ValueError("birthDate must be in the past")
        return v

class PatientUpdate(BaseModel):
    name: Optional[List[HumanName]] = None
    gender: Optional[str] = None
    birthDate: Optional[date] = None
    telecom: Optional[List[ContactPoint]] = None

class PatientResponse(PatientCreate):
    id: str = Field(..., description="FHIR resource ID")

class CKDPatientCreate(BaseModel):
    first_name: str = Field(..., description="Patient first name")
    last_name: str = Field(..., description="Patient last name")
    gender: str = Field(..., description="Patient gender")
    birth_date: date = Field(..., description="Patient birth date")
    ckd_stage: Optional[str] = Field("3", description="CKD stage (default: 3)")
    initial_labs: Optional[List[Dict]] = Field(None, description="Initial lab values (optional)")

    @field_validator('gender')
    @classmethod
    def gender_must_be_valid(cls, v):
        valid_genders = {'male', 'female', 'other', 'unknown'}
        if v.lower() not in valid_genders:
            raise ValueError(f"Invalid gender: {v}. Must be one of {valid_genders}")
        return v.lower()

    @field_validator('birth_date')
    @classmethod
    def birth_date_must_be_past(cls, v):
        if v >= date.today():
            raise ValueError("birth_date must be in the past")
        return v

class CKDPatientRegistrationResponse(BaseModel):
    patient_id: str = Field(..., description="FHIR Patient resource ID")
    condition_id: str = Field(..., description="FHIR Condition resource ID")
    message: str = Field(..., description="Operation result message")

class CKDSummaryResponse(BaseModel):
    patient: Dict = Field(..., description="FHIR Patient resource JSON")
    ckd_conditions: List[Dict] = Field(..., description="List of CKD Condition resources")
    latest_labs: List[Dict] = Field(..., description="List of latest lab Observation resources")
    summary: Dict = Field(..., description="Aggregated CKD summary data")

