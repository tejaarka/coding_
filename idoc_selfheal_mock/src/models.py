"""Pydantic models — structured contracts for agents and APIs.

Fill every TODO. Keep models small. Do not add database code here.
"""

from typing import Optional

from pydantic import BaseModel, Field


class IDocRef(BaseModel):
    """One row from the failed-IDoc poll feed."""

    docnum: str
    mestyp: str
    idoctyp: str
    status: str
    sector: str = ""
    error_message: str = ""
    xml: str = ""
    healable: Optional[bool] = None

    # TODO: add any extra fields you truly need from failed_idocs.json
    # (direct, intended_category, note). Prefer optional fields.


class Partner(BaseModel):
    parvw: str
    partner_id: str
    name: str = ""
    land1: str = ""


class LineItem(BaseModel):
    posex: str = ""
    menge: str = ""
    menee: str = ""
    werks: str = ""
    idtnr: str = ""
    netwr: str = ""


class IDocSummary(BaseModel):
    """Parsed view used by root-cause and resolution agents."""

    docnum: str
    status: str
    direct: str = ""
    mestyp: str = ""
    idoctyp: str = ""
    sndprn: str = ""
    rcvprn: str = ""
    error_message: str = ""
    partners: list[Partner] = Field(default_factory=list)
    items: list[LineItem] = Field(default_factory=list)
    # TODO: add optional header bits you need (delivery date, country, kunnr, ...)


class RootCauseResult(BaseModel):
    docnum: str
    category: str
    evidence: str
    confidence: float
    healable: bool
    sector: str = ""
    parvw: Optional[str] = None  # e.g. WE vs AG when relevant


class PatchProposal(BaseModel):
    docnum: str
    segment: str
    field: str
    old_value: str
    new_value: str
    reason: str
    confidence: float
    parvw: Optional[str] = None


class Approval(BaseModel):
    docnum: str
    approved: bool
    comment: str = ""
