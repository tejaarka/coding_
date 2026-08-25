"""Polling agent — triage nurse checking the waiting room.

Why: failed IDocs appear over time; do not re-open the same case forever.
"""

from src.models import IDocRef


_seen: set[str] = set()


def poll_new_failures() -> list[IDocRef]:
    """Use the *endpoint tool* to GET /idocs/failed.

    TODO:
    - call get_failed_idocs()
    - skip docnums already in _seen
    - add new docnums to _seen
    - return only new IDocRef objects
    """
    raise NotImplementedError("Step 6: polling agent")
