"""Root-cause agent — doctor who classifies, does not operate.

v1: RULES using data/classifications.json keywords + status.
v2 later: LLM with the SAME RootCauseResult model.

Why rules first: you need a baseline before trusting an LLM.
"""

from src.models import IDocRef, IDocSummary, RootCauseResult


def classify(ref: IDocRef, summary: IDocSummary) -> RootCauseResult:
    """TODO:

    1. If status in {53, 64}: healable=False, category SKIP or similar
    2. If status == 56: category PARTNER_PROFILE, healable=False
    3. Else match error_message (and maybe fields) against classification keywords
    4. If several keywords match, pick the most specific (e.g. ship-to over partner)
    5. If nothing matches: UNKNOWN, healable=False, confidence low
    6. Never set healable True for INVOICE_AMOUNT / PO_REFERENCE / PARTNER_PROFILE
    """
    raise NotImplementedError("Step 7: root-cause agent")
