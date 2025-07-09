from typing import Dict
from fhir.resources.observation import Observation
from app.utils.helpers import serialize_dates
from app.utils.exceptions import FHIRClientError
from .base_client import BaseFHIRClient
import json

class ObservationService(BaseFHIRClient):
    async def create_observation(self, observation_data: Dict) -> Dict:
        observation = Observation(**observation_data)
        serialized = serialize_dates(observation.dict())
        return await self._make_request("POST", "/Observation", serialized)

    async def get_observation(self, observation_id: str) -> Dict:
        return await self._make_request("GET", f"/Observation/{observation_id}")

    async def get_patient_observations(self, patient_id: str) -> Dict:
        return await self._make_request("GET", f"/Observation?subject=Patient/{patient_id}")

    async def update_observation(self, observation_id: str, observation_data: Dict) -> Dict:
        observation = Observation(**observation_data)
        serialized = serialize_dates(observation.dict())
        return await self._make_request("PUT", f"/Observation/{observation_id}", serialized)

    async def patch_observation(self, observation_id: str, observation_data: Dict) -> Dict:
        return await self._make_request("PATCH", f"/Observation/{observation_id}", observation_data)

    async def delete_observation(self, observation_id: str) -> Dict:
        return await self._make_request("DELETE", f"/Observation/{observation_id}")

