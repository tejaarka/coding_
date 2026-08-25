"""Simple orchestrator — charge nurse. Not Foundry.

Control flow only. Agents stay single-purpose.
If one IDoc fails, log and continue the others.
"""

from src.models import IDocRef


def handle_one(ref: IDocRef) -> str:
    """TODO pipeline:

    1. Load XML via idoc_reader (path from DATA_DIR / ref.xml) + error_message
    2. root_cause.classify(ref, summary)
    3. if not healable: return "escalated:{category}"
    4. patch = resolution.propose_patch(...)
    5. if patch is None: return "escalated:no_master"
    6. approval = hitl.ask_approval(patch)
    7. if not approval.approved: return "rejected"
    8. POST /idocs/{docnum}/reprocess with patch (via httpx or a small tool wrapper)
    9. return "reprocessed" or error text
    """
    raise NotImplementedError("Step 10: handle_one")


def run() -> None:
    """TODO: poll_new_failures(); for each ref, print handle_one(ref)."""
    raise NotImplementedError("Step 10: run")
