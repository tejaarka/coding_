# Revised Learning Roadmap — After Latest Team Discussion

**Status:** Roadmap **updated**. Day 3 (IDoc fundamentals) stays. Days 4+ are reordered.
**Why:** The team clarified the *real* Electrolux delivery shape: **orchestrator + agents + tools (API calls) + human-in-the-loop**, calling **SAP endpoints Electrolux will give us** — not deep SAP GUI / PyRFC / Basis work.

---

## 1. Are we on track?

| Area | Old roadmap | New team clarity | Verdict |
| --- | --- | --- | --- |
| IDoc format (structure, segments, status) | Day 3 focus | Team: “discover around IDoc only” | **Keep — on track** |
| Deep SAP (WE02/BD87/PyRFC/ABAP/Basis) | Heavy in Week 2 | Team: “no need to go deep into SAP”; mostly call their APIs | **Reduce sharply** |
| Azure Cosmos / Service Bus / App Service depth | Core P0 | Not confirmed for Electrolux environment | **Defer until they open access** |
| Agent + orchestrator + tools | Mentioned, later | Primary delivery model | **Move to P0 now** |
| Code tools vs endpoint tools | Not explicit | Explicit training topic | **Add as P0** |
| Human-in-the-loop | Mentioned | Confirmed in IDoc resolution path | **Keep / emphasize** |
| Foundry / MCP | Architecture awareness | May **not** get Foundry; MCP is a **server**, not a tool type; may write a **simple orchestrator** | **Awareness only until KT** |
| Only 2 use cases | IDoc + Web/Abaptum | **IDoc + API** only (MJ/NP) | **Rename second track to API** |
| Environment (Citrix done; Python/Git blocked) | Admin track | Ball in Electrolux’s court for software RFCs | **Monitor, don’t block learning** |

**Bottom line:** You are on track for **IDoc literacy**. You must **pivot learning time** from deep SAP/Azure infrastructure toward **agentic workflow design**: polling → root cause → resolution → human approve → reprocess via APIs.

---

## 2. What the IDoc use case actually is now

### Real-life analogy — hospital ER triage

Imagine a hospital emergency department:

1. **Polling agent** = triage nurse who keeps checking the waiting room for new patients (failed IDocs).
2. **Root cause agent** = doctor who reads the chart and classifies the problem (country code missing? delivery date wrong? material missing?).
3. **Master / lookup APIs** = lab + pharmacy systems that tell you the *correct* blood type / medicine (correct country code, correct customer, correct material).
4. **Resolution agent** = doctor who writes the corrected prescription (patched IDoc).
5. **Human-in-the-loop** = senior consultant who must **sign** before the prescription is applied.
6. **Orchestrator** = charge nurse who makes sure steps happen in order and nothing is skipped.
7. **SAP endpoint** = the hospital’s official patient record system you must read from and write back to.

You are not becoming a surgeon who builds the hospital (deep SAP). You are becoming the **ER team that uses the hospital’s APIs** to find, classify, fix (with approval), and resubmit cases.

### Technical workflow (confirmed from discussion)

```
SAP / Electrolux endpoint
        |
        v
[1] Polling Agent  ---- fetch failed IDocs / error dumps
        |
        v
[2] Read IDoc payload + error message
        |
        v
[3] Root Cause Agent  ---- classify into Electrolux categories
        |                   (country code, delivery date, material, partner, ...)
        v
[4] Resolution Agent  ---- call master/lookup APIs for correct values
        |                   (was 2 APIs, later 3 in Faisal's demo)
        v
[5] Human-in-the-loop ---- approve patch (UI / email / notification)
        |
        v
[6] Update IDoc + send back to SAP endpoint (reprocess)
        |
        v
   Orchestrator Agent owns the whole flow
```

### Two types of tools (critical)

| Tool type | Analogy | What it is | When used |
| --- | --- | --- | --- |
| **Endpoint-based tool** | Speed dial to one restaurant | Agent calls **one fixed API** with a prompt/payload | Simple, one service |
| **Code-based tool** | Personal assistant who can call many restaurants | You write **code** the agent runs; code can call **multiple endpoints**, branch, transform | Faisal’s pattern: 3 different APIs in one tool flow |

**MCP** = the **waiter station / tool server** that *hosts* tools. It is **not** a tool type. Don’t say “MCP tool type.”

Faisal’s earlier pattern (often 3 API steps):

1. **What failed?** — extract / confirm error from dump or IDoc  
2. **What should it be?** — compare against master / expected data  
3. **Resolution** — produce the fix using outputs of (1) + (2)

Electrolux may add more steps (sector-specific: manufacturing / finance / logistics) and always may insert **human confirmation**.

---

## 3. What to learn primarily (ordered)

Learn in this order. Do not skip levels.

### P0 — Learn now (blocks your contribution)

| # | Topic | Why | Analogy | Enough when you can… |
| --- | --- | --- | --- | --- |
| 1 | **IDoc structure (keep Day 3)** | You must read the failed document | Read a damaged shipping label | Point at control vs segments; name failing field |
| 2 | **Agent vs tool vs orchestrator** | Core delivery vocabulary | Doctor vs stethoscope vs charge nurse | Explain each in one sentence |
| 3 | **Endpoint tool vs code tool** | How AXIS tools are built | Speed dial vs multi-call assistant | Choose which type for a 3-API flow |
| 4 | **Multi-step tool calling** | Fail → expected → resolve | Lab then pharmacy then prescription | Design a 3-step tool plan for country-code error |
| 5 | **REST API calling** | Electrolux gives SAP APIs | Ordering by phone using a menu | Call an API with headers/JSON; handle errors |
| 6 | **Root-cause classification** | Categories Electrolux will share | Triage codes (trauma / cardiac /…) | Map an error text → category → next tool |
| 7 | **Human-in-the-loop** | Confirmed before IDoc update | Senior sign-off | Sketch approve/reject in the flow |
| 8 | **Simple orchestrator in code** | May not get Foundry | Charge nurse checklist in a script | Write a Python flow that runs agents in order |

### P1 — Learn during first project weeks

| Topic | Why | Analogy |
| --- | --- | --- |
| Prompting agents to call tools at the right step | Quality of diagnosis | Teaching a junior *when* to call the lab |
| Polling / retry / backoff | Failed IDoc feed | Checking waiting room every N minutes |
| Sector-aware prompts (finance / logistics / manufacturing) | Electrolux next complexity | Different wards need different protocols |
| Existing AXIS app KT (Dhruv backend / Rajiv UI) | Reuse patterns | Tour of a working clinic before building yours |
| API use-case KT | Second official use case | Second ward in the same hospital |

### P2 — Later / only if needed

| Topic | Why deferred |
| --- | --- |
| Deep SAP GUI (WE02, BD87, WE19) | You’ll call their APIs; GUI is nice-to-have |
| PyRFC / BAPI coding | Not the stated integration path |
| Azure Cosmos / Service Bus deep dive | Environment not confirmed |
| Foundry / MCP server authoring | May not be provided; wait for KT |
| Kubernetes / heavy DevOps | Not in current scope |
| ABAP dumps deep dive | Separate from IDoc path unless they expand scope |

### Explicitly do **not** over-invest now

- Installing Python/Git on Electrolux VDI yourself — **they** must raise RFCs  
- Inventing Electrolux error taxonomies — **they** will share classifications + endpoints  
- Building production Foundry graphs before you know the platform  

---

## 4. Concepts with dual examples (real life + project)

### 4.1 Orchestrator

- **Real life:** A wedding planner. Doesn’t cook or DJ; makes sure florist → caterer → photographer happen in order.  
- **Project:** Orchestrator agent starts polling, routes to root-cause agent by category, then resolution, then waits for human approval, then posts back to SAP.

### 4.2 Specialized agents

- **Real life:** Plumber vs electrician vs painter.  
- **Project:** Polling agent, root-cause agent, resolution agent — each with a narrow job.

### 4.3 Tools

- **Real life:** A mechanic’s wrenches. The mechanic (agent) decides which wrench; the wrench doesn’t decide.  
- **Project:** Tools wrap SAP “get failed IDocs”, “get master country code”, “submit corrected IDoc”.

### 4.4 Endpoint-based tool

- **Real life:** One dedicated hotline to the bank.  
- **Project:** Tool config points at a single REST URL; agent sends prompt/params; gets JSON back.

### 4.5 Code-based tool

- **Real life:** An assistant who can call the bank, the insurer, and the hospital, then summarize.  
- **Project:** Python function that calls API1 → API2 → API3, transforms fields, returns one structured result to the LLM.

### 4.6 Polling agent

- **Real life:** Refreshing a food-delivery app until the order shows “failed payment”.  
- **Project:** Periodically GET failed IDocs from Electrolux SAP endpoint; enqueue new ones.

### 4.7 Root cause agent

- **Real life:** Mechanic listens to the engine and says “it’s the battery, not the alternator.”  
- **Project:** Reads IDoc + error text; outputs category `COUNTRY_CODE_MISSING` / `DELIVERY_DATE_INVALID` / `MATERIAL_MISSING` / `PARTNER_INVALID`.

### 4.8 Resolution agent

- **Real life:** Mechanic replaces the battery with the correct part from inventory.  
- **Project:** Calls master API for correct country/customer/material; proposes IDoc field patch.

### 4.9 Human-in-the-loop

- **Real life:** Pharmacist must approve a high-risk prescription.  
- **Project:** Show old vs new IDoc field; human Approve / Reject / Edit; only then call update endpoint.

### 4.10 Classifications / sectors

- **Real life:** Fire department codes (medical / fire / hazmat) need different playbooks.  
- **Project:** Same IDoc platform, but manufacturing vs finance vs logistics errors need different prompts + different master APIs.

### 4.11 IDoc (still required, lightly)

- **Real life:** Damaged shipping form — you fix the address line, not the tracking barcode format.  
- **Project:** Patch `E1EDKA1-PARTN` or country field in data segments; don’t fake `STATUS`.

### 4.12 API use case (second track)

- **Real life:** A second hospital ward with different charts but same triage process.  
- **Project:** Separate Electrolux use case; wait for Dhruv/Rajiv KT; same agent/tool skills transfer.

---

## 5. New day-by-day plan (next 2–3 weeks)

Assumptions: ~2–3 hours/day; Citrix available; Python may be local until Electrolux VDI software is fixed; Electrolux endpoints/classifications may arrive mid-plan — practice with mocks until then.

### Week A — Foundations (agentic + IDoc refresh)

#### Day 1 — Reset the mental model
- **Topics:** IDoc vs API use cases only; orchestrator / agent / tool; MCP ≠ tool type.  
- **Analogy:** Hospital ER roles.  
- **Exercise:** One-page diagram of the IDoc workflow from the transcript.  
- **Output:** Diagram + 5 questions for Faisal/Arka (endpoints, classifications, HITL channel).  
- **Done when:** You can explain the workflow to a teammate in 2 minutes.

#### Day 2 — IDoc refresh (keep Day 3 asset)
- **Topics:** Control vs data vs status; 51 vs 53 vs 56 vs 64; ORDERS vs DEBMAS at a glance.  
- **Exercise:** Re-run `python3 day03-idoc-fundamentals/parse_idoc.py samples/`.  
- **Output:** For the failed ORDERS05, write “category guess” + “field to patch”.  
- **Done when:** You map one XML failure → a classification label in plain English.

#### Day 3 — REST API essentials for agents
- **Topics:** GET/POST, JSON, status codes, auth headers, timeouts, idempotency basics.  
- **Analogy:** Phone orders from a printed menu.  
- **Exercise:** Call a public JSON API (e.g. httpbin / JSONPlaceholder) with Python `requests` or `httpx`.  
- **Output:** Script `call_api_demo.py` with success + error handling.  
- **Done when:** You can explain how an agent tool wraps one HTTP call.

#### Day 4 — Endpoint tools vs code tools
- **Topics:** When to use each; Faisal’s 3-endpoint pattern.  
- **Exercise:** Implement **both**:
  1. Endpoint-style: function that calls one mock URL.
  2. Code-style: function that calls mock `/failed`, `/expected`, `/resolve` in sequence.
- **Output:** `tools/endpoint_tool.py`, `tools/code_tool.py`.  
- **Done when:** You can tell a teammate why code tools helped switch across 3 APIs.

#### Day 5 — Design the 3-step diagnostic for one error
- **Topics:** Country-code / delivery-date / material-missing examples.  
- **Exercise:** Pick “country code missing”. Write prompts + mock responses for steps 1–3.  
- **Output:** Markdown playbook `playbooks/country_code_missing.md`.  
- **Done when:** Playbook shows inputs/outputs between each API step.

### Week B — Build a mini orchestrator (mock Electrolux)

#### Day 6 — Polling agent
- **Topics:** Poll loop, “seen” IDoc ids, pagination, backoff.  
- **Analogy:** Checking the waiting room every 5 minutes.  
- **Exercise:** Mock endpoint returns failed IDocs; agent stores new ones only.  
- **Output:** `agents/polling_agent.py`.

#### Day 7 — Root cause agent
- **Topics:** Classification from error text + IDoc fields; controlled category enum.  
- **Exercise:** Rule-based first (if/else on keywords), optional LLM second.  
- **Output:** `agents/root_cause_agent.py` returning `{category, evidence, confidence}`.

#### Day 8 — Resolution agent + master lookup
- **Topics:** Call master API; propose patch `{segment, field, old, new}`.  
- **Exercise:** Mock master data for country/customer/material.  
- **Output:** `agents/resolution_agent.py`.

#### Day 9 — Human-in-the-loop gate
- **Topics:** Approve / reject / edit; never auto-post without gate (for Electrolux path).  
- **Exercise:** CLI or tiny web form showing old→new; block send until approved.  
- **Output:** `hitl/approval.py`.

#### Day 10 — Wire the orchestrator
- **Topics:** Sequential flow + failure handling (“if root cause unknown → escalate”).  
- **Exercise:** Single script: poll → classify → resolve → approve → “POST” mock SAP.  
- **Output:** `orchestrator/run_idoc_flow.py` + README demo script.  
- **Done when:** You can demo end-to-end on mock data.

### Week C — Soft skills for the real environment + API track

#### Day 11 — Prompt patterns for tool-calling agents
- **Topics:** System prompt: when to call which tool; pass prior tool output forward.  
- **Exercise:** Rewrite Day 5 playbook as agent instructions.  
- **Output:** `prompts/idoc_orchestrator_system.md`.

#### Day 12 — Sector-aware thinking (light)
- **Topics:** Same engine, different playbooks for manufacturing / finance / logistics.  
- **Exercise:** Create 3 category→tool routing tables (stubs).  
- **Output:** `playbooks/sectors.md`.  
- **Note:** Don’t invent Electrolux taxonomies — mark stubs as **placeholder until client provides**.

#### Day 13 — KT prep: AXIS app / Foundry-like demo
- **Topics:** Questions for Dhruv (backend) & Rajiv (UI).  
- **Exercise:** Prepare 10 KT questions (auth, tool registration, orchestrator storage, HITL UI).  
- **Output:** `questions/kt_dhruv_rajiv.md`.

#### Day 14 — API use-case orientation
- **Topics:** Second official use case; reuse orchestrator skills.  
- **Exercise:** One-pager comparing IDoc flow vs expected API-failure flow (unknowns listed).  
- **Output:** `notes/api_usecase_unknowns.md`.

#### Day 15 — Readiness dry-run
- **Topics:** Explain whole IDoc agent workflow + show mock demo.  
- **Exercise:** 10-minute talk + run orchestrator.  
- **Done when:** Teammate can follow your demo without the transcript.

---

## 6. Updated priority stack (wall chart)

```
1. Agent / Orchestrator / Tool mental model
2. Endpoint tool vs Code tool
3. REST API calling + JSON
4. IDoc read/parse (Day 3 — keep sharp)
5. Poll → Root cause → Resolve → HITL → Post back
6. Classification playbooks (wait for Electrolux list)
7. KT: existing app (Dhruv/Rajiv) + API use case
8. Platform specifics (Foundry/MCP) ONLY after they confirm
9. Deep SAP / deep Azure  — parking lot
```

---

## 7. What changed in your personal “do this week”

### Do immediately
1. Keep using Day 3 IDoc samples — still required.  
2. Start **agent + tools + orchestrator** practice with **mocks**.  
3. Watch Teams/Outlook for Electrolux notes.  
4. Join Dhruv KT when scheduled.  
5. Track VDI software blockers; don’t burn time fighting installs.

### Pause / shrink
1. PyRFC / live SAP GUI mastery.  
2. Cosmos DB / Service Bus deep labs.  
3. Building on Foundry before platform confirmation.

### Ask the team (high priority)
1. Will Electrolux give **REST endpoints** only, or also GUI/RFC?  
2. Exact **error classification list** and sample payloads?  
3. HITL channel: AXIS UI, email, Teams, or all?  
4. Do we implement orchestrator in **Foundry**, custom code, or both?  
5. Who owns **API use case** vs **IDoc use case** staffing?  
6. Timeline for Python/Git on Electrolux VDI?

---

## 8. Success criteria for “ready to contribute”

You are ready when you can:

- [ ] Explain IDoc use-case flow with the hospital analogy **and** technical names  
- [ ] Distinguish endpoint tool vs code tool vs MCP server  
- [ ] Read a failed IDoc XML and propose a category + field patch  
- [ ] Implement a mock 3-step tool chain (failed → expected → resolve)  
- [ ] Run a mini orchestrator with a human approval step  
- [ ] List what you are **waiting on** from Electrolux (endpoints, classifications, platform)

---

## 9. Relationship to Day 3 materials

| Asset | Still useful? | How |
| --- | --- | --- |
| `day03-idoc-fundamentals/STUDY_GUIDE.md` | Yes | Input literacy for root-cause agent |
| Sample XMLs + `parse_idoc.py` | Yes | Feed mock polling / classification |
| Deep WE02/BD87 day plans | De-prioritized | Optional if you get SAP GUI later |

Next lab folder to add when you start coding Week B: `idoc-agent-orchestrator-lab/` (mock APIs + agents + HITL).
