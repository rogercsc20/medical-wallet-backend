from typing import Dict
from fhir.resources.medication import Medication
from app.utils.helpers import serialize_dates
from app.utils.exceptions import FHIRClientError
from .base_client import BaseFHIRClient
import json

class MedicationService(BaseFHIRClient):
    async def create_medication(self, medication_data: Dict) -> Dict:
        if "manufacturer" in medication_data and medication_data["manufacturer"] is None:
            del medication_data["manufacturer"]
        medication = Medication(**medication_data)
        serialized = serialize_dates(medication.dict())
        return await self._make_request("POST", "/Medication", serialized)

    async def get_medication(self, medication_id: str) -> Dict:
        return await self._make_request("GET", f"/Medication/{medication_id}")

    async def update_medication(self, medication_id: str, medication_data: Dict) -> Dict:
        if "manufacturer" in medication_data and medication_data["manufacturer"] is None:
            del medication_data["manufacturer"]
        medication = Medication(**medication_data)
        serialized = serialize_dates(medication.dict())
        return await self._make_request("PUT", f"/Medication/{medication_id}", serialized)

    async def patch_medication(self, medication_id: str, medication_data: Dict) -> Dict:
        return await self._make_request("PATCH", f"/Medication/{medication_id}", medication_data)

    async def delete_medication(self, medication_id: str) -> Dict:
        return await self._make_request("DELETE", f"/Medication/{medication_id}")

