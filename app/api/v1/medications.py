import logging
from fastapi import APIRouter, Depends, HTTPException
from app.services.fhir_client import FHIRClient
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.medication import (
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=MedicationResponse,
    summary="Create new medication",
    description="Create a new medication record for a patient.",
    tags=["medications"],
)
async def create_medication(
    medication: MedicationCreate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.create_medication(medication.dict())
        logger.info(f"Medication created by user {current_user}: {result.get('id')}")
        return MedicationResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating medication: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to create medication.")

@router.get(
    "/{medication_id}",
    response_model=MedicationResponse,
    summary="Get medication by ID",
    description="Retrieve a specific medication by its FHIR ID.",
    tags=["medications"],
)
async def get_medication(
    medication_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.get_medication(medication_id)
        logger.info(f"Medication retrieved by user {current_user}: {medication_id}")
        return MedicationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving medication {medication_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="Medication not found")

@router.patch(
    "/{medication_id}",
    response_model=MedicationResponse,
    summary="Update medication (partial)",
    description="Partially update a medication.",
    tags=["medications"],
)
async def update_medication(
    medication_id: str,
    medication: MedicationUpdate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.update_medication(medication_id, medication.dict(exclude_unset=True))
        logger.info(f"Medication updated by user {current_user}: {medication_id}")
        return MedicationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error updating medication {medication_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to update medication")

@router.get(
    "/patient/{patient_id}",
    response_model=list[MedicationResponse],
    summary="List medications for patient",
    description="List all medications for a patient.",
    tags=["medications"],
)
async def list_patient_medications(
    patient_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        results = await fhir_client.get_patient_medications(patient_id)
        logger.info(f"Medications listed by user {current_user} for patient {patient_id}")
        return [MedicationResponse(**entry["resource"]) for entry in results.get("entry", [])]
    except FHIRClientError as e:
        logger.error(f"Error listing medications for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to list medications")

