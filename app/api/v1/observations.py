import logging
from fastapi import APIRouter, Depends, Query
from app.services.fhir.observation_service import ObservationService
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.observation import (
    ObservationCreate,
    ObservationUpdate,
    ObservationResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

def get_observation_service(fhir_client=Depends(get_fhir_client)):
    return ObservationService(
        base_url=fhir_client.base_url,
        timeout=fhir_client.timeout,
        auth_token=fhir_client.auth_token,
        client=fhir_client.client,
    )

@router.post(
    "/",
    response_model=ObservationResponse,
    summary="Create new observation (lab result)",
    description="Create a new lab result for a patient.",
    tags=["observations"],
)
async def create_observation(
    observation: ObservationCreate,
    observation_service: ObservationService = Depends(get_observation_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} creating observation")
    try:
        result = await observation_service.create_observation(observation.dict())
        return ObservationResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating observation: {str(e)}")
        raise

@router.get(
    "/{observation_id}",
    response_model=ObservationResponse,
    summary="Get observation by ID",
    description="Retrieve a specific lab result by its FHIR ID.",
    tags=["observations"],
)
async def get_observation(
    observation_id: str,
    observation_service: ObservationService = Depends(get_observation_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} retrieving observation {observation_id}")
    try:
        result = await observation_service.get_observation(observation_id)
        return ObservationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving observation {observation_id}: {str(e)}")
        raise FHIRClientError(f"Observation with ID {observation_id} not found.")

@router.get(
    "/patient/{patient_id}",
    response_model=list[ObservationResponse],
    summary="List observations for patient",
    description="List all lab results for a patient.",
    tags=["observations"],
)
async def list_patient_observations(
    patient_id: str,
    observation_service: ObservationService = Depends(get_observation_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} listing observations for patient {patient_id}")
    try:
        results = await observation_service.get_patient_observations(patient_id)
        entries = results.get("entry", [])
        return [ObservationResponse(**entry["resource"]) for entry in entries]
    except FHIRClientError as e:
        logger.error(f"Error listing observations for patient {patient_id}: {str(e)}")
        raise

@router.put(
    "/{observation_id}",
    response_model=ObservationResponse,
    summary="Update observation (full)",
    description="Update an entire lab result resource.",
    tags=["observations"],
)
async def update_observation(
    observation_id: str,
    observation: ObservationUpdate,
    observation_service: ObservationService = Depends(get_observation_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} updating observation {observation_id}")
    try:
        result = await observation_service.update_observation(observation_id, observation.dict())
        return ObservationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error updating observation {observation_id}: {str(e)}")
        raise

@router.patch(
    "/{observation_id}",
    response_model=ObservationResponse,
    summary="Patch observation (partial update)",
    description="Partially update a lab result.",
    tags=["observations"],
)
async def patch_observation(
    observation_id: str,
    observation: ObservationUpdate,
    observation_service: ObservationService = Depends(get_observation_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} patching observation {observation_id}")
    try:
        result = await observation_service.patch_observation(observation_id, observation.dict(exclude_unset=True))
        return ObservationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error patching observation {observation_id}: {str(e)}")
        raise

@router.delete(
    "/{observation_id}",
    response_model=dict,
    summary="Delete observation",
    description="Delete a lab result resource.",
    tags=["observations"],
)
async def delete_observation(
    observation_id: str,
    observation_service: ObservationService = Depends(get_observation_service),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"User {current_user} deleting observation {observation_id}")
    try:
        await observation_service.delete_observation(observation_id)
        return {"message": f"Observation {observation_id} deleted successfully."}
    except FHIRClientError as e:
        logger.error(f"Error deleting observation {observation_id}: {str(e)}")
        raise

