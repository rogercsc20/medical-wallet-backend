from typing import Dict
from fhir.resources.condition import Condition
from app.utils.helpers import serialize_dates
from app.utils.exceptions import FHIRClientError
from .base_client import BaseFHIRClient
import json

class ConditionService(BaseFHIRClient):
    async def create_condition(self, condition_data: Dict) -> Dict:
        condition = Condition(**condition_data)
        serialized = serialize_dates(condition.dict())
        return await self._make_request("POST", "/Condition", serialized)

    async def get_condition(self, condition_id: str) -> Dict:
        return await self._make_request("GET", f"/Condition/{condition_id}")

    async def get_patient_conditions(self, patient_id: str) -> Dict:
        return await self._make_request("GET", f"/Condition?subject=Patient/{patient_id}")

    async def update_condition(self, condition_id: str, condition_data: Dict) -> Dict:
        condition = Condition(**condition_data)
        serialized = serialize_dates(condition.dict())
        return await self._make_request("PUT", f"/Condition/{condition_id}", serialized)

    async def patch_condition(self, condition_id: str, condition_data: Dict) -> Dict:
        return await self._make_request("PATCH", f"/Condition/{condition_id}", condition_data)

    async def delete_condition(self, condition_id: str) -> Dict:
        return await self._make_request("DELETE", f"/Condition/{condition_id}")

