"""Endpoint-based tool: one function ≈ one HTTP API.

Analogy: a single speed-dial button.
"""

import httpx

from src.config import SAP_BASE_URL


def get_failed_idocs() -> list[dict]:
    """GET /idocs/failed

    TODO:
    - httpx.get(f"{SAP_BASE_URL}/idocs/failed", timeout=10.0)
    - raise on non-2xx (response.raise_for_status())
    - return JSON list
    """
    raise NotImplementedError("Step 5: endpoint tool get_failed_idocs")


def get_idoc(docnum: str) -> dict:
    """GET /idocs/{docnum} — still an endpoint tool (one URL)."""
    raise NotImplementedError("Step 5: endpoint tool get_idoc")
