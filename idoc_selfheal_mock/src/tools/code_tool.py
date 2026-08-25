"""Code-based tool: one function that calls several endpoints and glues results.

Analogy: an assistant who calls lab, then pharmacy, then summarizes.

This is Faisal's pattern: (1) what failed (2) what it should be (3) combined view.
"""

from src.models import IDocSummary, RootCauseResult


def diagnose_and_lookup(docnum: str, root_cause: RootCauseResult) -> dict:
    """Call multiple mock SAP APIs depending on category.

    TODO:
    1. GET /idocs/{docnum}  → failed payload / summary
    2. Based on root_cause.category, GET the matching master URL:
         PARTNER_INVALID / SHIP_TO_NOT_FOUND → /master/customers/{id}
         COUNTRY_CODE → /master/countries/{code}
         MATERIAL_MISSING → /master/materials/{id}
         UOM_MISMATCH → /master/uom/{unit}
         PLANT_INVALID → /master/plants/{werks}
    3. Return a dict:
         {"failed": ..., "expected": ..., "category": ...}
    4. If master 404: include {"expected": None, "error": "not found"}
       Do not invent values.

    Use httpx. Do not call resolution/reprocess here.
    """
    raise NotImplementedError("Step 5: code tool diagnose_and_lookup")
