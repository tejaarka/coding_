"""Tests — fill after Step 3+.

    python -m pip install pytest   # optional, not required on day 1
    pytest tests/test_idoc_reader.py
"""

from pathlib import Path

# TODO after you implement parse_idoc_xml:
# def test_sold_to_old_id():
#     summary = parse_idoc_xml(Path("data/idocs/ORDERS05_partner_old_soldto.xml"))
#     assert summary.docnum == "0000000123456789"
#     ag = next(p for p in summary.partners if p.parvw == "AG")
#     assert ag.partner_id == "CUST-OLD-12345"


def test_placeholder():
    assert True
