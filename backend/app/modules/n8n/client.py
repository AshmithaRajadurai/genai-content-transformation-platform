import logging
from typing import Any, Dict, Optional
import httpx

from backend.app.core.config import settings

logger = logging.getLogger("n8n_client")


class N8nClient:
    """
    Reusable HTTP Client for communicating with n8n webhook endpoints.
    Provides decoupled orchestration between FastAPI backend and n8n workflows.
    """

    def __init__(self, webhook_url: Optional[str] = None, timeout: float = 30.0):
        self.webhook_url = webhook_url or settings.N8N_WEBHOOK_URL
        self.timeout = timeout

    def is_configured(self) -> bool:
        """Checks if n8n webhook URL is configured."""
        return bool(self.webhook_url and self.webhook_url.strip())

    def trigger_workflow(
        self,
        payload: Dict[str, Any],
        custom_endpoint: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Sends payload to n8n webhook trigger.
        Returns parsed JSON response or None if offline/unconfigured.
        """
        url = custom_endpoint or self.webhook_url
        if not url:
            logger.debug("n8n webhook URL is not configured.")
            return None

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    return res.json()
                logger.warning("n8n webhook returned status code %s: %s", res.status_code, res.text)
                return None
        except Exception as exc:
            logger.warning("Failed to trigger n8n workflow at %s: %s", url, exc)
            return None


n8n_client = N8nClient()
