"""
Adapter skeleton for a real Jev (or compatible) API.

Replace the body of `call_jev` / `JevClient.evaluate` with an actual HTTP/SDK call.
The rest of the package expects:
    evaluator(state: str, questions: dict) -> dict
"""

from typing import Dict, Any, Optional
import os


class JevClient:
    """
    Minimal client. Configure via environment or constructor.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "jev",
        timeout: float = 60.0,
    ):
        self.api_key = api_key or os.getenv("JEV_API_KEY", "")
        self.base_url = base_url or os.getenv("JEV_BASE_URL", "https://api.example.com/v1")
        self.model = model
        self.timeout = timeout

    def evaluate(self, state: str, questions: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Call the real endpoint and return answers in the format expected by HierarchicalCatalog.

        Expected question types: noul, choice, score, monad (or post-process).
        """
        if not self.api_key:
            raise RuntimeError(
                "JEV_API_KEY is not set. "
                "Set the environment variable or pass api_key=..."
            )

        # ------------------------------------------------------------------
        # TODO: replace this block with a real request.
        # Example shape (adjust to the actual Jev API):
        #
        # import requests
        # resp = requests.post(
        #     f"{self.base_url}/evaluate",
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        #     json={
        #         "model": self.model,
        #         "state": state,
        #         "questions": questions,
        #     },
        #     timeout=self.timeout,
        # )
        # resp.raise_for_status()
        # return resp.json()["answers"]
        # ------------------------------------------------------------------

        raise NotImplementedError(
            "Implement the real Jev API call inside JevClient.evaluate(). "
            "See the TODO comment."
        )


def make_evaluator(client: Optional[JevClient] = None):
    """Return a callable compatible with HierarchicalCatalog.evaluate()."""
    client = client or JevClient()

    def evaluator(state: str, questions: Dict[str, Dict]) -> Dict[str, Any]:
        return client.evaluate(state, questions)

    return evaluator
