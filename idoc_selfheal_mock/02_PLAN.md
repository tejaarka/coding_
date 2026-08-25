# Plan — what to build, in order, and why

Work **one step at a time**. After each step: run something small, then ask me to review **that step’s files**.

Analogy: hospital ER (see `REVISED_ROADMAP.md`). This mock is a cardboard hospital with fake patients (IDocs).

---

## Architecture you will recreate (mock)

```
[dummy XML/JSON files]
        |
        v
[Mock SAP API - FastAPI]          <-- Electrolux SAP endpoints (unknown URLs)
   GET  /idocs/failed
   GET  /idocs/{docnum}
   GET  /master/customers/{id}
   GET  /master/materials/{id}
   GET  /master/countries/{code}
   POST /idocs/{docnum}/reprocess
        ^
        |  httpx  (endpoint tools + one code tool)
        |
[Polling agent] --> [Root-cause agent] --> [Resolution agent]
        |                                      |
        +-------- [Orchestrator] --------------+
                       |
                       v
              [HITL CLI approve/reject]
                       |
                       v
              POST reprocess (only if approved)
```

**Why FastAPI mock instead of real SAP?**  
Electrolux has not given endpoints. A local API still forces you to learn: HTTP, JSON contracts, status codes, retries, tool wrapping — the same skills as calling their API later.

**Why not Foundry/MCP in v1?**  
Team said platform is unknown. A Python orchestrator teaches the **flow**. You can later wrap the same functions as Foundry tools.

---

## Step 0 — Git (you)

From repo root:

```bash
git checkout -b feat/idoc-selfheal-mock
# after each completed step:
git add idoc_selfheal_mock
git commit -m "Step N: short description"
```

I will not commit unless you ask.

---

## Step 1 — Read the dummy data (no code)

**Files:** `data/README.md`, XMLs, `failed_idocs.json`, `master_data.json`, `classifications.json`

**Why:** Root-cause and resolution are only as good as the document you understood. Varied rows exist so you do not overfit to “customer ID wrong.”

**Your job:**
1. Open 3 XMLs (order, invoice, customer).
2. For each `failed_idocs.json` row, write on paper: status, sector, category guess, segment/field.
3. Note which rows must **not** be auto-healed (status 56, 64, 53, or config errors).

**Ask me to review:** your written mapping table (paste it). Not code yet.

---

## Step 2 — Config + shared models (`src/models.py`, `src/config.py`)

**Why Pydantic models?**  
Later the LLM must return **structured** patches (`segment`, `field`, `old`, `new`, `confidence`). If you start with dict soup, the orchestrator becomes untestable.

**Fill:** fields marked `TODO`. Do not invent extra layers.

**Run:** `python -c "from src.models import IDocRef, PatchProposal; print('models ok')"`  
(You may need `src/__init__.py` empty file — already provided.)

---

## Step 3 — IDoc reader (`src/idoc_reader.py`)

**Why:** Agents should not parse XML every time in ad-hoc ways. One reader → one summary object (docnum, mestyp, status, partners, items, error text).

**Reuse ideas** from `day03-idoc-fundamentals/parse_idoc.py` — **do not copy blindly**; write a function that returns `IDocSummary`.

**Run:** print summaries for all files in `data/idocs/`.

---

## Step 4 — Mock SAP API (`src/mock_sap/app.py`)

**Why:** This is the stand-in for “they will give us a SAP endpoint.” Polling and tools must not read files directly in the final design — they **call HTTP**. File access stays **inside** the mock server.

**Endpoints to implement (minimum):**

| Method | Path | Why |
| --- | --- | --- |
| GET | `/idocs/failed` | Polling agent feed |
| GET | `/idocs/{docnum}` | Read full IDoc + error |
| GET | `/master/customers/{id}` | Resolution lookup |
| GET | `/master/materials/{id}` | Resolution lookup |
| GET | `/master/countries/{code}` | Resolution lookup |
| POST | `/idocs/{docnum}/reprocess` | Send approved patch back |

**Run (you):**

```bash
uvicorn src.mock_sap.app:app --reload --port 8000
```

In another terminal: `curl http://127.0.0.1:8000/idocs/failed`

---

## Step 5 — Endpoint tool vs code tool (`src/tools/`)

**Why:** This is the concept from the team call. Implement **both**.

1. `endpoint_tool.py` — one function, one URL (e.g. get failed list).
2. `code_tool.py` — **one** function that internally calls:
   - what failed (`GET /idocs/{docnum}`)
   - what it should be (`GET /master/...`)
   - returns both blobs for the resolution step

**Do not** hide HTTP errors. Timeouts and 404s are part of the lesson.

---

## Step 6 — Polling agent (`src/agents/polling.py`)

**Why:** Failed IDocs arrive over time. Track `seen` docnums so you do not reprocess forever.

**Think twice:** at-least-once delivery (you may see the same IDoc twice). Store last poll cursor if the mock supports it (optional).

---

## Step 7 — Root-cause agent (`src/agents/root_cause.py`)

**v1 = rules, not LLM.**  
If error text contains `country` → `COUNTRY_CODE`. Map using `data/classifications.json`.

**Why rules first?**  
You need a **deterministic baseline**. LLM comes after you know categories and golden examples. Otherwise you cannot tell if the agent is wrong.

**Output:** `{category, evidence, confidence, healable: bool}`

Set `healable=False` for status 56/64/53 and for `PARTNER_PROFILE` / unknown.

---

## Step 8 — Resolution agent (`src/agents/resolution.py`)

**Why:** Classification without a patch is only a ticket label. Resolution calls master data and proposes **one field change** when possible.

**Think twice:** never invent a customer/material if master lookup 404s → escalate, don’t guess.

---

## Step 9 — HITL (`src/hitl/cli_approve.py`)

**Why:** Team confirmed approval before updating the IDoc.

Print old vs new; wait for `y/n`. No means skip POST.

---

## Step 10 — Orchestrator (`src/orchestrator.py`)

**Why:** This is the “simple orchestrator code” Faisal/team said you might write if not Foundry.

Wire: poll → for each new idoc → root cause → if healable: resolve → HITL → reprocess.

**Think twice:** if any step fails, **stop that IDoc**, log, continue the others. Don’t crash the whole run.

---

## Step 11 — Manual demo script

`python -m src.run_demo`

Show one healable IDoc (customer old id) and one non-healable (status 56).

---

## Later (only after demo works)

- Optional LLM classify using the same `RootCauseResult` model  
- pytest for reader + classifier  
- Tiny web HITL  
- Map functions to MCP/Foundry **after** KT  

---

## What “done” looks like for this mock

- [ ] Mock SAP running locally  
- [ ] Poll returns mixed statuses and types  
- [ ] Classifier labels at least: partner, country, delivery date, material, UoM, finance invoice, config  
- [ ] Code tool performs 2–3 HTTP calls  
- [ ] HITL blocks reprocess on `n`  
- [ ] Approved patch hits `POST /reprocess` and mock status becomes 53  
- [ ] You can explain each folder to a teammate with the ER analogy  
