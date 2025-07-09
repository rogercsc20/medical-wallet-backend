import logging
from fastapi import APIRouter, Depends, HTTPException
from app.services.fhir_client import FHIRClient
from app.services.ckd_service import CKDService
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.patient import (
    PatientCreate,
    PatientResponse,
    CKDPatientCreate,
    CKDPatientRegistrationResponse,
    CKDSummaryResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=PatientResponse,
    summary="Create a new patient",
    description="Register a new patient in the FHIR server.",
    tags=["patients"],
)
async def create_patient(
    patient: PatientCreate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.create_patient(patient.dict())
        logger.info(f"Patient created by user {current_user}: {result.get('id')}")
        return PatientResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating patient: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to create patient.")

@router.post(
    "/ckd",
    response_model=CKDPatientRegistrationResponse,
    summary="Register CKD patient",
    description="Register a new CKD patient, including initial diagnosis and labs.",
    tags=["patients"],
)
async def register_ckd_patient(
    patient: CKDPatientCreate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        ckd_service = CKDService(fhir_client)
        result = await ckd_service.register_ckd_patient(patient.dict())
        logger.info(f"CKD patient registered by user {current_user}: {result.get('patient_id')}")
        return CKDPatientRegistrationResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error registering CKD patient: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to register CKD patient.")

@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Get patient by ID",
    description="Retrieve a patient's FHIR resource by their unique ID.",
    tags=["patients"],
)
async def get_patient(
    patient_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.get_patient(patient_id)
        logger.info(f"Patient retrieved by user {current_user}: {patient_id}")
        return PatientResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="Patient not found")

@router.get(
    "/{patient_id}/ckd-summary",
    response_model=CKDSummaryResponse,
    summary="Get CKD summary for patient",
    description="Aggregate and return CKD-specific summary for a patient.",
    tags=["patients"],
)
async def get_ckd_summary(
    patient_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        ckd_service = CKDService(fhir_client)
        result = await ckd_service.get_ckd_summary(patient_id)
        logger.info(f"CKD summary retrieved by user {current_user}: {patient_id}")
        return CKDSummaryResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving CKD summary for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="Patient not found")

