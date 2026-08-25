# Contract — what you do vs what I do vs what is research

This mock exists so you touch the **same technical shapes** as Electrolux IDoc self-heal: polling, classification, tools (endpoint + code), master lookup, human approval, reprocess, orchestrator.

It is **not** production SAP, Foundry, or Electrolux’s real taxonomy.

---

## You do (human / you)

| Work | Why it must be you |
| --- | --- |
| Install Python/Git/packages on **your** machine | Environment is yours; Electrolux VDI RFCs are theirs |
| Create git commits on **your** cadence | You asked to version this yourself |
| Fill every `TODO` in `src/` | Learning happens when you write the flow |
| Decide category names until Electrolux publishes theirs | Their list is unknown; ours are **placeholders** |
| Write prompts later (when/if you add an LLM) | Prompt quality is iterative human judgment |
| HITL product choice (CLI now; UI/email later) | Electrolux channel unknown (AXIS UI vs email vs Teams) |
| Confidence thresholds (auto vs ask human) | Business policy, not a coding trick |
| Validate whether a patch is **safe** | Guardrails need domain + client rules |
| Attend Dhruv/Faisal KT and map this mock to real tools | Real platform may differ (Foundry vs custom) |

---

## I can do (when you **ask**)

| Work | Limit |
| --- | --- |
| Review **your** file: bugs, naming, missing steps | One step at a time — not a rewrite of the whole repo |
| Suggest a better function signature or test case | After you attempted it |
| Explain why a design is risky | Concepts in `03_CRITICAL_CONCEPTS.md` |
| Help debug a traceback you paste | Need your error + the file you wrote |
| Later: optional LLM wiring **if** you choose a provider | You must supply key + policy |
| Later: tiny FastAPI polish after your first working mock | Only after your orchestrator runs on dummy data |

I will **not** fill `TODO`s in advance. I will **not** commit to git unless you explicitly ask.

---

## I cannot honestly implement (research / client / humans)

These are **not** things a coding assistant can finish for Electrolux:

1. **Real Electrolux error classification list** — Faisal said they will share categories with the SAP endpoint. Anything in `data/classifications.json` is a **guess** for practice.
2. **Real SAP APIs** — paths, auth (OAuth vs basic vs certificates), payloads, pagination, rate limits. Wait for their spec.
3. **Which fields are legally/process-safe to auto-patch** — country code vs price vs partner may have different approval rules.
4. **Foundry vs custom orchestrator vs MCP hosting** — team said they may **not** get Foundry. Don’t lock the mock to Foundry.
5. **True LLM accuracy on messy dumps** — extracting “what failed” from unstructured ABAP/IDoc text needs samples from **their** dumps, evaluation, and prompt iteration.
6. **Human-in-the-loop channel** — UI vs email vs “another platform” is a client decision.
7. **Sector playbooks** (manufacturing / finance / logistics) — they said this is the *next* complexity; no real data yet.
8. **Master-data authority** — which system is source of truth for customer/material/country (MDG, ECC, S/4). We mock a `master_data.json`.
9. **Idempotency in real SAP** — reprocessing twice must not create duplicate orders. Needs their reprocess semantics.
10. **Security / secrets on Electrolux domain** — Key Vault, managed identity, VDI software RFCs.

Treat anything I generate as **training wheels**, not client truth.

---

## Build rule

```
You implement step N  →  you run it  →  you ask "correct this file"
I review only that step  →  you commit
```

Never skip to “write the whole orchestrator for me.”
