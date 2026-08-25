"""Resolution agent — proposes a single field patch from master lookup.

Does not POST reprocess. Does not ask the human. Orchestrator does that.
"""

from src.models import IDocSummary, PatchProposal, RootCauseResult


def propose_patch(summary: IDocSummary, root_cause: RootCauseResult) -> PatchProposal | None:
    """TODO:

    - call code_tool.diagnose_and_lookup(summary.docnum, root_cause)
    - if expected is missing: return None (escalate)
    - map category → segment/field/old/new (see classifications.json)
    - SHIP_TO_NOT_FOUND must use PARVW=WE partner, not AG
    - PARTNER_INVALID sold-to: PARVW=AG; consider mentioning RE uses same old id
    - confidence: 0.9 if mapping exists, lower if heuristic
    """
    raise NotImplementedError("Step 8: resolution agent")
