"""Parse IDoc XML into IDocSummary.

Why: one reader so agents never scrape XML ad hoc.

You may look at day03-idoc-fundamentals/parse_idoc.py for ideas.
Do not copy it wholesale — return IDocSummary, not print statements.
"""

from pathlib import Path

from src.models import IDocSummary


def parse_idoc_xml(path: Path, error_message: str = "") -> IDocSummary:
    """Parse one XML file.

    TODO:
    - load XML (xml.etree.ElementTree is enough)
    - read EDI_DC40 control fields
    - collect E1EDKA1 partners (PARVW, PARTN or LIFNR, LAND1, NAME1)
    - collect E1EDP01 items + nested E1EDP19 IDTNR
    - if DEBMAS, read E1KNA1M KUNNR
    - attach error_message from the catalog (XML usually has no EDIDS)
    """
    raise NotImplementedError("Step 3: implement parse_idoc_xml")
