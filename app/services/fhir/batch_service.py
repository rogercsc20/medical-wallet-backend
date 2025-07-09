import logging
from typing import Dict, Any
from .base_client import BaseFHIRClient
from app.utils.exceptions import FHIRClientError

logger = logging.getLogger(__name__)

class BatchService(BaseFHIRClient):
    async def batch_request(self, bundle: Dict[str, Any]) -> Dict:
        """
        Execute a FHIR $batch operation (Bundle of type 'batch' or 'transaction').
        :param bundle: FHIR Bundle resource (type must be 'batch' or 'transaction')
        """
        if bundle.get("resourceType") != "Bundle" or bundle.get("type") not in ["batch", "transaction"]:
            logger.error("Invalid bundle for FHIR $batch operation")
            raise FHIRClientError("Bundle must have resourceType='Bundle' and type='batch' or 'transaction'.")

        try:
            response = await self._make_request("POST", "/Bundle", bundle)
            logger.info("FHIR $batch operation executed successfully.")
            return response
        except Exception as e:
            logger.error(f"Error executing FHIR $batch: {str(e)}")
            raise FHIRClientError(f"Error executing FHIR $batch: {str(e)}")

    async def export_ndjson(self, resource_type: str, params: Dict[str, str] = None) -> Dict:
        """
        Initiate a FHIR bulk data export (NDJSON format).
        :param resource_type: FHIR resource type (e.g., 'Patient')
        :param params: Optional query parameters for filtering
        """
        endpoint = f"/{resource_type}/$export"
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"?{query_string}"

        try:
            response = await self._make_request("GET", endpoint)
            logger.info(f"FHIR bulk export for {resource_type} initiated.")
            return response
        except Exception as e:
            logger.error(f"Error initiating FHIR bulk export: {str(e)}")
            raise FHIRClientError(f"Error initiating FHIR bulk export: {str(e)}")

    async def import_ndjson(self, resource_type: str, ndjson_data: str) -> Dict:
        """
        Import NDJSON data as FHIR resources (for bulk import).
        :param resource_type: FHIR resource type (e.g., 'Patient')
        :param ndjson_data: NDJSON string (newline-delimited JSON)
        """
        endpoint = f"/{resource_type}/$import"
        headers = self.headers.copy()
        headers["Content-Type"] = "application/fhir+ndjson"

        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = await self.client.post(
                url,
                headers=headers,
                content=ndjson_data
            )
            response.raise_for_status()
            logger.info(f"FHIR bulk import for {resource_type} executed.")
            return response.json()
        except Exception as e:
            logger.error(f"Error executing FHIR bulk import: {str(e)}")
            raise FHIRClientError(f"Error executing FHIR bulk import: {str(e)}")

