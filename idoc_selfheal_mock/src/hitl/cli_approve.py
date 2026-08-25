"""Human-in-the-loop — senior sign-off before the IDoc is changed.

v1: CLI. Do not skip this to make the demo 'automatic'.
"""

from src.models import Approval, PatchProposal


def ask_approval(patch: PatchProposal) -> Approval:
    """TODO:

    Print docnum, category reason, segment, field, old → new.
    Read input y/n (and optional comment).
    Return Approval(approved=..., comment=...)
    Default if empty input: not approved (fail safe).
    """
    raise NotImplementedError("Step 9: HITL CLI")
