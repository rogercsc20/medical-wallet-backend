class FHIRClientError(Exception):
    """Custom exception for FHIR client errors"""
    pass

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class PatientNotFoundError(Exception):
    """Custom exception for patient not found"""
    pass

