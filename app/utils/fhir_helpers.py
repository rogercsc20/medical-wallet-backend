from typing import Dict
from datetime import datetime

def create_ckd_condition(patient_id: str, stage: str = "3") -> Dict:
    """Create a CKD condition FHIR resource"""
    stage_codes = {
        "1": {"code": "431855005", "display": "Chronic kidney disease stage 1"},
        "2": {"code": "431856006", "display": "Chronic kidney disease stage 2"},
        "3": {"code": "700379002", "display": "Chronic kidney disease stage 3B"},
        "4": {"code": "431857002", "display": "Chronic kidney disease stage 4"},
        "5": {"code": "431858007", "display": "Chronic kidney disease stage 5"}
    }
    
    return {
        "resourceType": "Condition",
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                    "display": "Active"
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed",
                    "display": "Confirmed"
                }
            ]
        },
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                        "code": "problem-list-item",
                        "display": "Problem List Item"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": stage_codes.get(stage, stage_codes["3"])["code"],
                    "display": stage_codes.get(stage, stage_codes["3"])["display"]
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "recordedDate": datetime.now().isoformat()
    }

def create_lab_observation(patient_id: str, lab_data: Dict) -> Dict:
    """Create a lab observation FHIR resource"""
    lab_codes = {
        "creatinine": {"code": "33914-3", "display": "Creatinine [Mass/volume] in Serum or Plasma"},
        "egfr": {"code": "48642-3", "display": "Glomerular filtration rate/1.73 sq M.predicted [Volume Rate/Area] in Serum or Plasma by Creatinine-based formula (CKD-EPI)"},
        "bun": {"code": "14682-9", "display": "Creatinine [Moles/volume] in Serum or Plasma"}
    }
    
    lab_type = lab_data.get("type", "creatinine")
    
    return {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "laboratory",
                        "display": "Laboratory"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": lab_codes[lab_type]["code"],
                    "display": lab_codes[lab_type]["display"]
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "effectiveDateTime": lab_data.get("date", datetime.now().isoformat()),
        "valueQuantity": {
            "value": lab_data["value"],
            "unit": lab_data.get("unit", "mg/dL"),
            "system": "http://unitsofmeasure.org"
        }
    }

