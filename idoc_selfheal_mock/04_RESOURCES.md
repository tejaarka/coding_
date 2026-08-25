# Public resources this mock is based on

Use these while filling templates. None of them are Electrolux-internal.

## IDoc structure and status

- [SAP IDoc Guide — read an IDoc, status 51, WE02/BD87](https://keyusertraining.com/en/sap-idoc-guide/)  
  Status 51 = application document not posted; message text is the real clue.
- [IDoc status overview (inbound 50–75)](https://www.munich-enterprise.com/en/sap-idoc-status)  
  51 / 53 / 56 / 64 meanings.
- [INVOIC02 composition and segments (ecosio)](https://ecosio.com/en/blog/composition-and-structure-of-a-invoic-idoc-in-sap-erp/)  
  Control `EDI_DC40`, header `E1EDK*`, items `E1EDP*`, totals `E1EDS01`.
- [ORDERS05 segment/field catalogue](https://beyondse16.com/2020/04/16/complete-segment-and-field-list-of-sap-idoc-orders05-purchasing-sales/)  
  `E1EDKA1-PARVW/PARTN`, `E1EDP01-MENGE/MENEE`, `E1EDP19-IDTNR`.
- [DEBMAS customer IDoc (community)](https://community.sap.com/t5/technology-blog-posts-by-members/customer-idoc-debmas-simplified/ba-p/13260732)  
  `E1KNA1M-KUNNR`, company code / sales views.

## HTTP / FastAPI / tools (your mock platform)

- [FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [httpx quickstart](https://www.python-httpx.org/)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)

## Agentic pattern (conceptual, not vendor lock-in)

- Tool calling / structured outputs (OpenAI cookbook — only when you add an LLM later)
- Your team transcript: **endpoint tool vs code tool**; 3-step fail → expected → resolve; orchestrator; HITL

## What we did **not** copy

- No live SAP system, no PyRFC
- No Azure Foundry / MCP requirement in v1
- No Electrolux dump files (we synthesized realistic **error messages** instead)
