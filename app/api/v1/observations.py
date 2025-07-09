import logging
from fastapi import APIRouter, Depends, HTTPException
from app.services.fhir_client import FHIRClient
from app.core.dependencies import get_fhir_client, get_current_user
from app.schemas.observation import (
    ObservationCreate,
    ObservationUpdate,
    ObservationResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post(
    "/",
    response_model=ObservationResponse,
    summary="Create new observation (lab result)",
    description="Create a new lab result for a patient.",
    tags=["observations"],
)
async def create_observation(
    observation: ObservationCreate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.create_observation(observation.dict())
        logger.info(f"Observation created by user {current_user}: {result.get('id')}")
        return ObservationResponse(**result)
    except (FHIRClientError, ValidationError) as e:
        logger.error(f"Error creating observation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to create observation.")

@router.get(
    "/{observation_id}",
    response_model=ObservationResponse,
    summary="Get observation by ID",
    description="Retrieve a specific lab result by its FHIR ID.",
    tags=["observations"],
)
async def get_observation(
    observation_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.get_observation(observation_id)
        logger.info(f"Observation retrieved by user {current_user}: {observation_id}")
        return ObservationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error retrieving observation {observation_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="Observation not found")

@router.patch(
    "/{observation_id}",
    response_model=ObservationResponse,
    summary="Update observation (partial)",
    description="Partially update a lab result.",
    tags=["observations"],
)
async def update_observation(
    observation_id: str,
    observation: ObservationUpdate,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        result = await fhir_client.update_observation(observation_id, observation.dict(exclude_unset=True))
        logger.info(f"Observation updated by user {current_user}: {observation_id}")
        return ObservationResponse(**result)
    except FHIRClientError as e:
        logger.error(f"Error updating observation {observation_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to update observation")

@router.get(
    "/patient/{patient_id}",
    response_model=list[ObservationResponse],
    summary="List observations for patient",
    description="List all lab results for a patient.",
    tags=["observations"],
)
async def list_patient_observations(
    patient_id: str,
    fhir_client: FHIRClient = Depends(get_fhir_client),
    current_user: str = Depends(get_current_user),
):
    try:
        results = await fhir_client.get_patient_observations(patient_id)
        logger.info(f"Observations listed by user {current_user} for patient {patient_id}")
        return [ObservationResponse(**entry["resource"]) for entry in results.get("entry", [])]
    except FHIRClientError as e:
        logger.error(f"Error listing observations for patient {patient_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to list observations")

