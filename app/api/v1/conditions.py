import logging
from fastapi import APIRouter, Depends, Query
from app.services.fhir.condition_service import ConditionService
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.condition import (
    ConditionCreate,
    ConditionUpdate,
    ConditionResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

def get_condition_service(fhir_client=Depends(get_fhir_client)):
    return ConditionService(
        base_url=fhir_client.base_url,
        timeout=fhir_client.timeout,
        auth_token=fhir_client.auth_token,
        client=fhir_client.client,
    )

@router.post(
    "/",
    response_model=ConditionResponse,
    summary="Create new condition",
    description="Create a new condition record for a patient.",
    tags=["conditions"],
)
async def create_condition(
    condition: ConditionCreate,
    condition_service: ConditionService = Depends(get_condition_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} creating condition")
    try:
        result = await condition_service.create_condition(condition.dict())
        return ConditionResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating condition: {str(e)}")
        raise

@router.get(
    "/{condition_id}",
    response_model=ConditionResponse,
    summary="Get condition by ID",
    description="Retrieve a specific condition by its FHIR ID.",
    tags=["conditions"],
)
async def get_condition(
    condition_id: str,
    condition_service: ConditionService = Depends(get_condition_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} retrieving condition {condition_id}")
    try:
        result = await condition_service.get_condition(condition_id)
        return ConditionResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving condition {condition_id}: {str(e)}")
        raise FHIRClientError(f"Condition with ID {condition_id} not found.")

@router.get(
    "/patient/{patient_id}",
    response_model=list[ConditionResponse],
    summary="List conditions for patient",
    description="List all conditions for a patient.",
    tags=["conditions"],
)
async def list_patient_conditions(
    patient_id: str,
    condition_service: ConditionService = Depends(get_condition_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} listing conditions for patient {patient_id}")
    try:
        results = await condition_service.get_patient_conditions(patient_id)
        entries = results.get("entry", [])
        return [ConditionResponse(**entry["resource"]) for entry in entries]
    except FHIRClientError as e:
        logger.error(f"Error listing conditions for patient {patient_id}: {str(e)}")
        raise

@router.put(
    "/{condition_id}",
    response_model=ConditionResponse,
    summary="Update condition (full)",
    description="Update an entire condition resource.",
    tags=["conditions"],
)
async def update_condition(
    condition_id: str,
    condition: ConditionUpdate,
    condition_service: ConditionService = Depends(get_condition_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} updating condition {condition_id}")
    try:
        result = await condition_service.update_condition(condition_id, condition.dict())
        return ConditionResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error updating condition {condition_id}: {str(e)}")
        raise

@router.patch(
    "/{condition_id}",
    response_model=ConditionResponse,
    summary="Patch condition (partial update)",
    description="Partially update a condition resource.",
    tags=["conditions"],
)
async def patch_condition(
    condition_id: str,
    condition: ConditionUpdate,
    condition_service: ConditionService = Depends(get_condition_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} patching condition {condition_id}")
    try:
        result = await condition_service.patch_condition(condition_id, condition.dict(exclude_unset=True))
        return ConditionResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error patching condition {condition_id}: {str(e)}")
        raise

@router.delete(
    "/{condition_id}",
    response_model=dict,
    summary="Delete condition",
    description="Delete a condition resource.",
    tags=["conditions"],
)
async def delete_condition(
    condition_id: str,
    condition_service: ConditionService = Depends(get_condition_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} deleting condition {condition_id}")
    try:
        await condition_service.delete_condition(condition_id)
        return {"message": f"Condition {condition_id} deleted successfully."}
    except FHIRClientError as e:
        logger.error(f"Error deleting condition {condition_id}: {str(e)}")
        raise

