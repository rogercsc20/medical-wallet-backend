import logging
from fastapi import APIRouter, Depends, HTTPException
from app.services.fhir_client import FHIRClient
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.condition import (
    ConditionCreate,
    ConditionUpdate,
    ConditionResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=ConditionResponse,
    summary="Create new condition (diagnosis)",
    description="Create a new diagnosis for a patient.",
    tags=["conditions"],
)
async def create_condition(
    condition: ConditionCreate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.create_condition(condition.dict())
        logger.info(f"Condition created by user {current_user}: {result.get('id')}")
        return ConditionResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating condition: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to create condition.")

@router.get(
    "/{condition_id}",
    response_model=ConditionResponse,
    summary="Get condition by ID",
    description="Retrieve a specific diagnosis by its FHIR ID.",
    tags=["conditions"],
)
async def get_condition(
    condition_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.get_condition(condition_id)
        logger.info(f"Condition retrieved by user {current_user}: {condition_id}")
        return ConditionResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving condition {condition_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="Condition not found")

@router.patch(
    "/{condition_id}",
    response_model=ConditionResponse,
    summary="Update condition (partial)",
    description="Partially update a diagnosis.",
    tags=["conditions"],
)
async def update_condition(
    condition_id: str,
    condition: ConditionUpdate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.update_condition(condition_id, condition.dict(exclude_unset=True))
        logger.info(f"Condition updated by user {current_user}: {condition_id}")
        return ConditionResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error updating condition {condition_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to update condition")

@router.get(
    "/patient/{patient_id}",
    response_model=list[ConditionResponse],
    summary="List conditions for patient",
    description="List all diagnoses for a patient.",
    tags=["conditions"],
)
async def list_patient_conditions(
    patient_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        results = await fhir_client.get_patient_conditions(patient_id)
        logger.info(f"Conditions listed by user {current_user} for patient {patient_id}")
        return [ConditionResponse(**entry["resource"]) for entry in results.get("entry", [])]
    except FHIRClientError as e:
        logger.error(f"Error listing conditions for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to list conditions")

