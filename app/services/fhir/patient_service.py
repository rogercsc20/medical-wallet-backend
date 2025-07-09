from typing import Dict
from fhir.resources.patient import Patient
from app.utils.helpers import serialize_dates
from app.utils.exceptions import FHIRClientError
from .base_client import BaseFHIRClient
import json

class PatientService(BaseFHIRClient):
    async def create_patient(self, patient_data: Dict) -> Dict:
        patient = Patient(**patient_data)
        serialized = serialize_dates(patient.dict())
        return await self._make_request("POST", "/Patient", serialized)

    async def get_patient(self, patient_id: str) -> Dict:
        return await self._make_request("GET", f"/Patient/{patient_id}")

    async def search_patients(self, params: Dict[str, str]) -> Dict:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return await self._make_request("GET", f"/Patient?{query_string}")

    async def update_patient(self, patient_id: str, patient_data: Dict) -> Dict:
        patient = Patient(**patient_data)
        serialized = serialize_dates(patient.dict())
        return await self._make_request("PUT", f"/Patient/{patient_id}", serialized)

    async def patch_patient(self, patient_id: str, patient_data: Dict) -> Dict:
        return await self._make_request("PATCH", f"/Patient/{patient_id}", patient_data)

    async def delete_patient(self, patient_id: str) -> Dict:
        return await self._make_request("DELETE", f"/Patient/{patient_id}")

