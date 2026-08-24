#!/usr/bin/env python3
"""Parse SAP IDoc XML and print control record, segments, and business mapping.

Usage:
    python3 parse_idoc.py samples/ORDERS05_failed_status51.xml
    python3 parse_idoc.py samples/
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CONTROL_FIELDS = (
    "DOCNUM",
    "STATUS",
    "DIRECT",
    "MESTYP",
    "IDOCTYP",
    "SNDPRN",
    "RCVPRN",
    "SNDPRT",
    "RCVPRT",
    "CREDAT",
    "CRETIM",
)

SEGMENT_MEANING = {
    "EDI_DC40": "Control record (envelope: sender, receiver, type, status)",
    "E1EDK01": "Document header general data (currency, action, document number)",
    "E1EDKA1": "Header partner (sold-to / ship-to / bill-to / vendor)",
    "E1EDK02": "Header reference documents (for example PO number)",
    "E1EDK03": "Header dates",
    "E1EDK14": "Header organizational data (sales org, channel, division)",
    "E1EDP01": "Line item general data (quantity, unit, price, plant)",
    "E1EDP19": "Line item object identification (material number)",
    "E1EDP26": "Line item amounts",
    "E1EDS01": "Document totals / summary",
    "E1KNA1M": "Customer general master (KNA1) — number, name, country, account group",
    "E1KNB1M": "Customer company-code master (KNB1) — needed for FI posting",
    "E1KNVVM": "Customer sales-area master (KNVV) — needed for SD orders",
}

PARTNER_FUNCTION = {
    "AG": "Sold-to party",
    "WE": "Ship-to party",
    "RE": "Bill-to party",
    "RG": "Payer",
    "LF": "Vendor",
    "RS": "Invoice issuer",
}

STATUS_MEANING = {
    "01": "IDoc created",
    "03": "Data passed to port",
    "12": "Dispatch OK",
    "51": "Application document not posted (business error)",
    "53": "Application document posted (success)",
    "56": "IDoc added with errors (syntax / partner / structure)",
    "64": "IDoc ready to be transferred to application",
    "68": "Error — no further processing",
}

DIRECTION_MEANING = {
    "1": "Outbound (this SAP is sending)",
    "2": "Inbound (this SAP is receiving / posting)",
}

CONTROL_SKIP = {"TABNAM", "MANDT", "DOCREL", "CIMTYP", "MESCOD", "MESFCT", "SERIAL"}


def local_tag(element: ET.Element) -> str:
    tag = element.tag
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def child_text(element: ET.Element, name: str) -> str:
    for child in element:
        if local_tag(child) == name and child.text:
            return child.text.strip()
    return ""


def is_segment(element: ET.Element) -> bool:
    return element.attrib.get("SEGMENT") == "1" or local_tag(element) == "EDI_DC40"


def walk_segments(parent: ET.Element, depth: int = 0) -> list[tuple[int, ET.Element]]:
    found: list[tuple[int, ET.Element]] = []
    for child in parent:
        if is_segment(child):
            found.append((depth, child))
            found.extend(walk_segments(child, depth + 1))
        else:
            found.extend(walk_segments(child, depth))
    return found


def field_map(segment: ET.Element) -> dict[str, str]:
    values: dict[str, str] = {}
    for child in segment:
        if is_segment(child):
            continue
        name = local_tag(child)
        if child.text and child.text.strip():
            values[name] = child.text.strip()
    return values


def parse_idoc(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    idoc = root.find("IDOC")
    if idoc is None:
        # Some exports use the root as IDOC
        idoc = root if local_tag(root) == "IDOC" else root

    print("=" * 72)
    print(f"FILE          {path.name}")
    print(f"ROOT (type)   {local_tag(root)}")
    print("=" * 72)

    control = None
    for element in idoc.iter():
        if local_tag(element) == "EDI_DC40":
            control = element
            break

    if control is None:
        print("No EDI_DC40 control record found.")
        return

    print("\nCONTROL RECORD  (EDIDC / EDI_DC40)")
    print("-" * 72)
    fields = field_map(control)
    for name in CONTROL_FIELDS:
        value = fields.get(name, "")
        extra = ""
        if name == "STATUS":
            extra = f"  -> {STATUS_MEANING.get(value, 'see WE02')}"
        elif name == "DIRECT":
            extra = f"  -> {DIRECTION_MEANING.get(value, '')}"
        elif name == "MESTYP":
            extra = "  -> business intent (message type)"
        elif name == "IDOCTYP":
            extra = "  -> technical structure (IDoc type / version)"
        print(f"  {name:<8} {value}{extra}")

    print("\nDATA SEGMENTS  (EDID4)")
    print("-" * 72)
    partners: list[dict[str, str]] = []
    items: list[dict[str, str]] = []
    customer: dict[str, str] = {}

    for depth, segment in walk_segments(idoc):
        name = local_tag(segment)
        if name in {"IDOC", "EDI_DC40"}:
            continue
        indent = "  " * depth
        meaning = SEGMENT_MEANING.get(name, "Unmapped segment — look up in WE60")
        fields = field_map(segment)
        summary = ""
        if name == "E1EDKA1":
            parvw = fields.get("PARVW", "")
            partner_id = fields.get("PARTN") or fields.get("LIFNR", "")
            summary = f" | {PARTNER_FUNCTION.get(parvw, parvw)} = {partner_id}"
            partners.append(fields)
        elif name == "E1EDP01":
            summary = (
                f" | item {fields.get('POSEX', '?')} "
                f"qty {fields.get('MENGE', '?')} {fields.get('MENEE', '')}"
            )
            items.append(fields)
        elif name == "E1EDP19":
            summary = f" | material {fields.get('IDTNR', '')}"
            if items:
                items[-1]["IDTNR"] = fields.get("IDTNR", "")
        elif name == "E1KNA1M":
            summary = f" | customer {fields.get('KUNNR', '')} {fields.get('NAME1', '')}"
            customer = fields
        elif name == "E1KNB1M":
            summary = f" | company code {fields.get('BUKRS', '')}"
        elif name == "E1KNVVM":
            summary = (
                f" | sales area {fields.get('VKORG', '')}/"
                f"{fields.get('VTWEG', '')}/{fields.get('SPART', '')}"
            )
        print(f"{indent}{name:<10} {meaning}{summary}")

    print("\nBUSINESS READ-OUT")
    print("-" * 72)
    print(f"  Message        {fields_get(control, 'MESTYP')}  ({fields_get(control, 'IDOCTYP')})")
    print(f"  Direction      {DIRECTION_MEANING.get(fields_get(control, 'DIRECT'), '')}")
    print(f"  Current status {fields_get(control, 'STATUS')} "
          f"({STATUS_MEANING.get(fields_get(control, 'STATUS'), '')})")
    print(f"  Route          {fields_get(control, 'SNDPRN')} -> {fields_get(control, 'RCVPRN')}")

    if partners:
        print("  Partners")
        for partner in partners:
            parvw = partner.get("PARVW", "")
            partner_id = partner.get("PARTN") or partner.get("LIFNR", "")
            print(
                f"    - {parvw} {PARTNER_FUNCTION.get(parvw, ''):<16} "
                f"{partner_id:<20} {partner.get('NAME1', '')}"
            )
    if items:
        print("  Line items")
        for item in items:
            print(
                f"    - {item.get('POSEX', '?')}  "
                f"{item.get('IDTNR', '(no material segment)')}  "
                f"qty {item.get('MENGE', '?')} {item.get('MENEE', '')}  "
                f"net {item.get('NETWR', '')} {item.get('CURCY', '')}"
            )
    if customer:
        print(
            f"  Customer master {customer.get('KUNNR')}  "
            f"{customer.get('NAME1')}  account group {customer.get('KTOKD')}"
        )

    print("\nSELF-HEAL HINT")
    print("-" * 72)
    status = fields_get(control, "STATUS")
    sold_to = next((p for p in partners if p.get("PARVW") == "AG"), None)
    if status == "51" and sold_to and sold_to.get("PARTN", "").startswith("CUST-OLD"):
        print("  Likely failure field:  E1EDKA1 (PARVW=AG) / PARTN")
        print(f"  Current value:        {sold_to.get('PARTN')}")
        print("  Why:                  inbound ORDERS in status 51 with a sold-to")
        print("                        number that looks like a pre-migration ID.")
        print("  Typical patch:        map CUST-OLD-* to the new customer number,")
        print("                        then reprocess (BD87) until status 53.")
    elif status == "51":
        print("  Status 51 = application refused to post. Inspect partners,")
        print("  materials, plants, and org data against SAP master data.")
    elif status == "64":
        print("  Status 64 = received, not yet posted. Not a business error yet.")
    elif status == "53":
        print("  Status 53 = posted successfully. No heal required.")
    elif status == "56":
        print("  Status 56 = structure/partner-profile problem. Usually NOT a")
        print("  field patch — escalate as ALE/EDI configuration.")
    print()


def fields_get(control: ET.Element, name: str) -> str:
    return field_map(control).get(name, "")


def collect_xml_files(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(target.glob("*.xml"))
    if target.is_file():
        return [target]
    raise FileNotFoundError(target)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        here = Path(__file__).resolve().parent
        target = here / "samples"
        print("No path given — parsing ./samples\n")
    else:
        target = Path(argv[1])

    files = collect_xml_files(target)
    if not files:
        print(f"No XML files found at {target}")
        return 1

    for xml_file in files:
        parse_idoc(xml_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
