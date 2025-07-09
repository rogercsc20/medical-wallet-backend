import logging
from fastapi import APIRouter, Depends, Query
from app.services.fhir.medication_service import MedicationService
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.medication import (
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

def get_medication_service(fhir_client=Depends(get_fhir_client)):
    return MedicationService(
        base_url=fhir_client.base_url,
        timeout=fhir_client.timeout,
        auth_token=fhir_client.auth_token,
        client=fhir_client.client,
    )

@router.post(
    "/",
    response_model=MedicationResponse,
    summary="Create new medication",
    description="Create a new medication record for a patient.",
    tags=["medications"],
)
async def create_medication(
    medication: MedicationCreate,
    medication_service: MedicationService = Depends(get_medication_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} creating medication")
    try:
        result = await medication_service.create_medication(medication.dict())
        return MedicationResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating medication: {str(e)}")
        raise

@router.get(
    "/{medication_id}",
    response_model=MedicationResponse,
    summary="Get medication by ID",
    description="Retrieve a specific medication by its FHIR ID.",
    tags=["medications"],
)
async def get_medication(
    medication_id: str,
    medication_service: MedicationService = Depends(get_medication_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} retrieving medication {medication_id}")
    try:
        result = await medication_service.get_medication(medication_id)
        return MedicationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving medication {medication_id}: {str(e)}")
        raise FHIRClientError(f"Medication with ID {medication_id} not found.")

@router.get(
    "/patient/{patient_id}",
    response_model=list[MedicationResponse],
    summary="List medications for patient",
    description="List all medications for a patient.",
    tags=["medications"],
)
async def list_patient_medications(
    patient_id: str,
    medication_service: MedicationService = Depends(get_medication_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} listing medications for patient {patient_id}")
    try:
        results = await medication_service._make_request("GET", f"/Medication?subject=Patient/{patient_id}")
        entries = results.get("entry", [])
        return [MedicationResponse(**entry["resource"]) for entry in entries]
    except FHIRClientError as e:
        logger.error(f"Error listing medications for patient {patient_id}: {str(e)}")
        raise

@router.put(
    "/{medication_id}",
    response_model=MedicationResponse,
    summary="Update medication (full)",
    description="Update an entire medication resource.",
    tags=["medications"],
)
async def update_medication(
    medication_id: str,
    medication: MedicationUpdate,
    medication_service: MedicationService = Depends(get_medication_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} updating medication {medication_id}")
    try:
        result = await medication_service.update_medication(medication_id, medication.dict())
        return MedicationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error updating medication {medication_id}: {str(e)}")
        raise

@router.patch(
    "/{medication_id}",
    response_model=MedicationResponse,
    summary="Patch medication (partial update)",
    description="Partially update a medication resource.",
    tags=["medications"],
)
async def patch_medication(
    medication_id: str,
    medication: MedicationUpdate,
    medication_service: MedicationService = Depends(get_medication_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} patching medication {medication_id}")
    try:
        result = await medication_service.patch_medication(medication_id, medication.dict(exclude_unset=True))
        return MedicationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error patching medication {medication_id}: {str(e)}")
        raise

@router.delete(
    "/{medication_id}",
    response_model=dict,
    summary="Delete medication",
    description="Delete a medication resource.",
    tags=["medications"],
)
async def delete_medication(
    medication_id: str,
    medication_service: MedicationService = Depends(get_medication_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} deleting medication {medication_id}")
    try:
        await medication_service.delete_medication(medication_id)
        return {"message": f"Medication {medication_id} deleted successfully."}
    except FHIRClientError as e:
        logger.error(f"Error deleting medication {medication_id}: {str(e)}")
        raise

