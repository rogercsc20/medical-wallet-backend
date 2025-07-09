import logging
from fastapi import APIRouter, Depends, Query
from app.services.fhir.patient_service import PatientService
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError, PatientNotFoundError

router = APIRouter()
logger = logging.getLogger(__name__)

def get_patient_service(fhir_client=Depends(get_fhir_client)):
    return PatientService(
        base_url=fhir_client.base_url,
        timeout=fhir_client.timeout,
        auth_token=fhir_client.auth_token,
        client=fhir_client.client,
    )

@router.post(
    "/",
    response_model=PatientResponse,
    summary="Create patient",
    description="Create a new patient FHIR resource.",
    tags=["patients"],
)
async def create_patient(
    patient: PatientCreate,
    patient_service: PatientService = Depends(get_patient_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} creating patient")
    try:
        result = await patient_service.create_patient(patient.dict())
        return PatientResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating patient: {str(e)}")
        raise

@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Get patient by ID",
    description="Retrieve a patient's FHIR resource by their unique ID.",
    tags=["patients"],
)
async def get_patient(
    patient_id: str,
    patient_service: PatientService = Depends(get_patient_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} retrieving patient {patient_id}")
    try:
        result = await patient_service.get_patient(patient_id)
        return PatientResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving patient {patient_id}: {str(e)}")
        raise PatientNotFoundError(f"Patient with ID {patient_id} not found.")

@router.get(
    "/",
    response_model=list[PatientResponse],
    summary="Search patients",
    description="Search for patients by query parameters.",
    tags=["patients"],
)
async def search_patients(
    name: str = Query(None, description="Patient name"),
    identifier: str = Query(None, description="Patient identifier"),
    patient_service: PatientService = Depends(get_patient_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} searching patients")
    try:
        params = {}
        if name:
            params["name"] = name
        if identifier:
            params["identifier"] = identifier
        results = await patient_service.search_patients(params)
        entries = results.get("entry", [])
        return [PatientResponse(**entry["resource"]) for entry in entries]
    except FHIRClientError as e:
        logger.error(f"Error searching patients: {str(e)}")
        raise

@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Update patient (full)",
    description="Update an entire patient FHIR resource.",
    tags=["patients"],
)
async def update_patient(
    patient_id: str,
    patient: PatientUpdate,
    patient_service: PatientService = Depends(get_patient_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} updating patient {patient_id}")
    try:
        result = await patient_service.update_patient(patient_id, patient.dict())
        return PatientResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error updating patient {patient_id}: {str(e)}")
        raise

@router.patch(
    "/{patient_id}",
    response_model=PatientResponse,
    summary="Patch patient (partial update)",
    description="Partially update a patient FHIR resource.",
    tags=["patients"],
)
async def patch_patient(
    patient_id: str,
    patient: PatientUpdate,
    patient_service: PatientService = Depends(get_patient_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} patching patient {patient_id}")
    try:
        result = await patient_service.patch_patient(patient_id, patient.dict(exclude_unset=True))
        return PatientResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error patching patient {patient_id}: {str(e)}")
        raise

@router.delete(
    "/{patient_id}",
    response_model=dict,
    summary="Delete patient",
    description="Delete a patient FHIR resource.",
    tags=["patients"],
)
async def delete_patient(
    patient_id: str,
    patient_service: PatientService = Depends(get_patient_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} deleting patient {patient_id}")
    try:
        result = await patient_service.delete_patient(patient_id)
        return {"message": f"Patient {patient_id} deleted successfully."}
    except FHIRClientError as e:
        logger.error(f"Error deleting patient {patient_id}: {str(e)}")
        raise

