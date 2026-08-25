# Critical concepts — think twice, learn with focus

These are the pieces that will hurt the real Electrolux build if you treat them as “just more Python.”

---

## 1. Healable vs not healable (highest stakes)

**Analogy:** A pharmacist can correct a missing dosage unit. They must **not** silently rewrite a legal consent form.

| Usually healable (after HITL) | Usually **not** a field patch |
| --- | --- |
| Wrong/missing country code | Status **56** partner profile / ALE config |
| Old customer number with master mapping | Status **64** (not failed yet) |
| Material number typo with master hit | Status **53** already posted |
| UoM `PC` vs `EA` if mapping exists | Missing partner profile, port, RFC |
| Delivery date format / obvious invalid date | Duplicate posting / locking / authorization |

If you auto-heal config errors, you teach the agent to **lie** (edit payload instead of fixing WE20).

**Focus exercise:** Label every row in `failed_idocs.json` as `HEAL` / `ESCALATE` / `SKIP` **before** you code.

---

## 2. Structured outputs, not free text

**Analogy:** Lab results come as `blood_type: A+`, not a poem.

Root cause and resolution must be objects:

```text
category: COUNTRY_CODE
segment: E1EDKA1
field: LAND1
old: XX
new: SE
confidence: 0.0–1.0
healable: true|false
```

If you return paragraphs, HITL and reprocess cannot be reliable. This is the same discipline you will need for LLM **function calling**.

---

## 3. Endpoint tool vs code tool (from the team call)

**Think twice before making everything an endpoint tool.**

- One URL, no branching → endpoint tool.  
- Need fail **and** expected **and** glue logic → **code tool**.

Faisal used a code tool because **three** endpoints depended on each other. If you only make three separate endpoint tools, the LLM/orchestrator must remember to call them in order and pass outputs. That is fragile. A code tool can enforce order in Python.

**Focus:** implement both; use the code tool for the diagnostic triplet.

---

## 4. Don’t patch the control record status

**Analogy:** You don’t mark a package “delivered” with a Sharpie. You fix the address and send it again.

`EDI_DC40/STATUS = 51` is a **result**. The mock reprocess endpoint should set 53 **after** accepting a valid patch. Your resolution agent patches **data segments**.

---

## 5. Idempotency and “seen” IDocs

**Analogy:** Don’t admit the same patient twice and amputate twice.

Polling will return the same failed IDoc until SAP status changes. You need:

- an in-memory (then file) set of `docnum` already in flight  
- after successful reprocess, next poll should not treat it as new (mock should drop it from `/failed`)

Real SAP: reprocess twice might **duplicate a business document**. You cannot fully simulate that here — flag it as research.

---

## 6. Master data 404 = escalate, never invent

**Analogy:** If the pharmacy doesn’t have the drug, you don’t cook a random substitute.

If `GET /master/customers/CUST-OLD-12345` has a mapping, use `mapped_to`. If the id is unknown, `healable=False`.

Hallucinated customer numbers are the #1 way an LLM “self-heal” becomes dangerous.

---

## 7. One IDoc, many partners

`E1EDKA1` repeats. `PARVW=AG` vs `WE` vs `RE` are different people.

**Think twice:** error “ship-to not found” → patch `WE`, not `AG`. Your sample data includes this trap.

---

## 8. Confidence and HITL policy

Even a correct mapping may require a human if:

- confidence &lt; threshold  
- field is financial (`NETWR`, tax)  
- category is `UNKNOWN`  
- multiple fields need changes  

**You** pick a threshold (e.g. 0.95 auto-propose but **still HITL** in this mock, because Electrolux confirmed HITL on resolution). Do not skip HITL in v1 “to make the demo smoother.”

---

## 9. Orchestrator owns control flow, agents stay dumb

**Analogy:** Charge nurse sequences rooms; the lab does not decide the surgery.

Root-cause agent should **not** call reprocess. Resolution should **not** poll. If you mix them, you cannot replace one agent later with an LLM.

---

## 10. Mock contracts will change

When Electrolux sends a real OpenAPI spec, your `mock_sap` routes will be wrong. Keep HTTP **behind** `src/tools/` so you change URLs in one place.

**Focus:** no `httpx.get` scattered inside agents except via tools.
