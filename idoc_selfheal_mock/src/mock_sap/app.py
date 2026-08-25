"""Mock SAP HTTP API — stand-in for Electrolux endpoints.

Why: polling and tools must call HTTP, not open files directly.

Run (after you implement):
    uvicorn src.mock_sap.app:app --reload --port 8000
"""

from fastapi import FastAPI

app = FastAPI(title="Mock SAP IDoc API")

# TODO: load data/failed_idocs.json and data/master_data.json once at startup
# TODO: keep an in-memory copy so POST /reprocess can change status


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/idocs/failed")
def list_failed_idocs():
    """Return IDocs that look failed (status 51 or 56). Exclude 53 and 64.

    TODO: implement. Shape: list of dicts matching IDocRef.
    """
    raise NotImplementedError("Step 4: GET /idocs/failed")


@app.get("/idocs/{docnum}")
def get_idoc(docnum: str):
    """Return catalog row + parsed XML summary (or raw xml path).

    TODO: 404 if unknown.
    """
    raise NotImplementedError("Step 4: GET /idocs/{docnum}")


@app.get("/master/customers/{customer_id}")
def get_customer(customer_id: str):
    """TODO: lookup master_data.json customers. 404 if missing."""
    raise NotImplementedError("Step 4: GET /master/customers/{id}")


@app.get("/master/materials/{material_id}")
def get_material(material_id: str):
    raise NotImplementedError("Step 4: GET /master/materials/{id}")


@app.get("/master/countries/{code}")
def get_country(code: str):
    raise NotImplementedError("Step 4: GET /master/countries/{code}")


@app.get("/master/uom/{unit}")
def get_uom(unit: str):
    """TODO: map PC -> EA using master_data.uom_map."""
    raise NotImplementedError("Step 4: GET /master/uom/{unit}")


@app.get("/master/plants/{werks}")
def get_plant(werks: str):
    raise NotImplementedError("Step 4: GET /master/plants/{werks}")


@app.post("/idocs/{docnum}/reprocess")
def reprocess(docnum: str, payload: dict):
    """Accept an approved PatchProposal-like body.

    TODO:
    - reject if IDoc not healable / unknown
    - set status to 53 in memory
    - return {docnum, status: "53"}
    Do NOT trust the client to send status 53 without a patch body.
    """
    raise NotImplementedError("Step 4: POST /idocs/{docnum}/reprocess")
