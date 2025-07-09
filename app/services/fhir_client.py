import logging
import httpx
from typing import Dict, Optional, Any
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.condition import Condition
from fhir.resources.medication import Medication
from app.utils.exceptions import FHIRClientError
from app.core.config import settings
from app.utils.helpers import serialize_dates
import json

logger = logging.getLogger(__name__)

class FHIRClient:
    def __init__(self, base_url: str, timeout: int = 30, auth_token: Optional[str] = None, client: Optional[httpx.AsyncClient] = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.auth_token = auth_token
        self.client = client or httpx.AsyncClient(timeout=self.timeout)
        self.headers = {
            "Content-Type": "application/fhir+json",
            "Accept": "application/fhir+json"
        }
        if self.auth_token:
            self.headers["Authorization"] = f"Bearer {self.auth_token}"

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to FHIR server"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = await self.client.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            logger.info(f"FHIR {method} {url} success")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"FHIR server error: {e.response.status_code} on {url}")
            raise FHIRClientError(f"FHIR server error: {e.response.status_code}")
        except httpx.TimeoutException:
            logger.error(f"FHIR server timeout on {url}")
            raise FHIRClientError("FHIR server timeout")
        except Exception as e:
            logger.error(f"FHIR client error on {url}: {str(e)}")
            raise FHIRClientError(f"FHIR client error: {str(e)}")

    async def create_patient(self, patient_data: Dict) -> Dict:
        patient = Patient(**patient_data)
        serialized = serialize_dates(patient.dict())
        logger.info(f"FHIR payload: {json.dumps(serialized)}")
        return await self._make_request("POST", "/Patient", serialized)

    async def get_patient(self, patient_id: str) -> Dict:
        return await self._make_request("GET", f"/Patient/{patient_id}")

    async def search_patients(self, params: Dict[str, str]) -> Dict:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return await self._make_request("GET", f"/Patient?{query_string}")

    async def create_observation(self, observation_data: Dict) -> Dict:
        observation = Observation(**observation_data)
        serialized = serialize_dates(observation.dict())
        return await self._make_request("POST", "/Observation", serialized)
    
    async def get_observation(self, observation_id: str) -> dict:
        return await self._make_request("GET", f"/Observation/{observation_id}")

    async def get_patient_observations(self, patient_id: str) -> Dict:
        return await self._make_request("GET", f"/Observation?subject=Patient/{patient_id}")

    async def create_condition(self, condition_data: Dict) -> Dict:
        condition = Condition(**condition_data)
        serialized = serialize_dates(condition.dict())
        return await self._make_request("POST", "/Condition", serialized)
    
    async def get_condition(self, condition_id: str) -> dict:
        return await self._make_request("GET", f"/Condition/{condition_id}")

    async def get_patient_conditions(self, patient_id: str) -> Dict:
        return await self._make_request("GET", f"/Condition?subject=Patient/{patient_id}")

    async def create_medication(self, medication_data: Dict) -> Dict:
        if "manufacturer" in medication_data and medication_data["manufacturer"] is None:
            del medication_data["manufacturer"]
        medication = Medication(**medication_data)
        serialized = serialize_dates(medication.dict())
        return await self._make_request("POST", "/Medication", serialized)

    async def get_medication(self, medication_id: str) -> dict:
        return await self._make_request("GET", f"/Medication/{medication_id}")


