import logging
from typing import Dict, List
from app.services.fhir.base_client import BaseFHIRClient
from app.utils.fhir_helpers import create_ckd_condition, create_lab_observation
from app.constants.clinical import CKD_CODES, CKD_LAB_CODES
from app.schemas.patient import (
    CKDPatientCreate,
    CKDPatientRegistrationResponse,
    CKDSummaryResponse,
)
from app.utils.exceptions import FHIRClientError, ValidationError
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class CKDService:
    def __init__(self, fhir_client: BaseFHIRClient):
        self.fhir_client = fhir_client

    async def register_ckd_patient(self, patient_data: CKDPatientCreate) -> CKDPatientRegistrationResponse:
        """Register a new CKD patient with initial data"""
        try:
            # Create patient
            patient_fhir = {
                "resourceType": "Patient",
                "name": [{"family": patient_data.last_name, "given": [patient_data.first_name]}],
                "gender": patient_data.gender,
                "birthDate": str(patient_data.birth_date)
            }
            patient_result = await self.fhir_client.create_patient(patient_fhir)
            patient_id = patient_result["id"]

            # Create CKD condition
            ckd_condition = create_ckd_condition(patient_id, patient_data.ckd_stage)
            condition_result = await self.fhir_client.create_condition(ckd_condition)

            # Create initial lab values in parallel if provided
            if patient_data.initial_labs:
                tasks = [
                    self.fhir_client.create_observation(create_lab_observation(patient_id, lab))
                    for lab in patient_data.initial_labs
                ]
                await asyncio.gather(*tasks)

            logger.info(f"CKD patient registered: patient_id={patient_id}, condition_id={condition_result['id']}")
            return CKDPatientRegistrationResponse(
                patient_id=patient_id,
                condition_id=condition_result["id"],
                message="CKD patient registered successfully"
            )
        except (FHIRClientError, ValidationError) as e:
            logger.error(f"Error registering CKD patient: {str(e)}")
            raise

    async def get_ckd_summary(self, patient_id: str) -> CKDSummaryResponse:
        """Get CKD summary for a patient"""
        try:
            patient = await self.fhir_client.get_patient(patient_id)
            conditions = await self.fhir_client.get_patient_conditions(patient_id)
            observations = await self.fhir_client.get_patient_observations(patient_id)

            ckd_conditions = self._filter_ckd_conditions(conditions)
            latest_labs = self._get_latest_ckd_labs(observations)
            summary = self._generate_ckd_summary(ckd_conditions, latest_labs)

            logger.info(f"CKD summary generated for patient_id={patient_id}")
            return CKDSummaryResponse(
                patient=patient,
                ckd_conditions=ckd_conditions,
                latest_labs=latest_labs,
                summary=summary
            )
        except FHIRClientError as e:
            logger.error(f"Error retrieving CKD summary for patient {patient_id}: {str(e)}")
            raise

    def _filter_ckd_conditions(self, conditions: Dict) -> List[Dict]:
        """Filter conditions to only CKD-related ones"""
        ckd_codes = {v["code"] for v in CKD_CODES.values()}
        filtered = []
        if "entry" in conditions:
            for entry in conditions["entry"]:
                condition = entry["resource"]
                if condition.get("code", {}).get("coding"):
                    for coding in condition["code"]["coding"]:
                        if coding.get("code") in ckd_codes:
                            filtered.append(condition)
                            break
        return filtered

    def _get_latest_ckd_labs(self, observations: Dict) -> List[Dict]:
        """Get latest CKD-related lab results"""
        ckd_lab_codes = set(CKD_LAB_CODES.values())
        latest_labs = []
        if "entry" in observations:
            for entry in observations["entry"]:
                observation = entry["resource"]
                if observation.get("code", {}).get("coding"):
                    for coding in observation["code"]["coding"]:
                        if coding.get("code") in ckd_lab_codes:
                            latest_labs.append(observation)
                            break
        # Sort by date and get latest
        return sorted(latest_labs, key=lambda x: x.get("effectiveDateTime", ""), reverse=True)[:5]

    def _generate_ckd_summary(self, ckd_conditions: List[Dict], latest_labs: List[Dict]) -> Dict:
        """Generate CKD summary with stage and recommendations"""
        # Example: Calculate stage from latest eGFR
        stage = "unknown"
        egfr = None
        for obs in latest_labs:
            for coding in obs.get("code", {}).get("coding", []):
                if coding.get("code") == CKD_LAB_CODES["egfr"]:
                    egfr = obs.get("valueQuantity", {}).get("value")
                    break
        if egfr is not None:
            if egfr >= 90:
                stage = "1"
            elif egfr >= 60:
                stage = "2"
            elif egfr >= 45:
                stage = "3A"
            elif egfr >= 30:
                stage = "3B"
            elif egfr >= 15:
                stage = "4"
            else:
                stage = "5"
        return {
            "ckd_stage": stage,
            "risk_level": "Moderate" if stage in {"3A", "3B", "4"} else "Low" if stage in {"1", "2"} else "High",
            "recommendations": [
                "Monitor blood pressure regularly",
                "Follow nephrology appointments",
                "Maintain protein-restricted diet"
            ]
        }

