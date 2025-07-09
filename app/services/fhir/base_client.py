import logging
import httpx
from typing import Dict, Optional, Any
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

