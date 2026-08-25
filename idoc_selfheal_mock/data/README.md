# Dummy data guide

All IDocs here are **synthetic**, shaped like real SAP XML (ORDERS05, INVOIC02, DEBMAS06) plus a JSON catalog the mock API can serve without parsing XML on every poll.

## Files

| File | Role |
| --- | --- |
| `idocs/*.xml` | Full envelopes (control + data segments) |
| `failed_idocs.json` | Poll feed: metadata + error message + sector (what dumps/APIs would add) |
| `master_data.json` | Lookup APIs: customers, materials, countries, UoM map |
| `classifications.json` | **Placeholder** categories until Electrolux publishes theirs |

## Variety matrix (what you should notice)

| docnum | Type | Status | Sector | Intended category | Healable? |
| --- | --- | --- | --- | --- | --- |
| 0000000123456789 | ORDERS05 | 51 | logistics | PARTNER_INVALID (old sold-to) | yes, HITL |
| 0000000123456790 | ORDERS05 | 51 | logistics | SHIP_TO_NOT_FOUND | yes, patch WE not AG |
| 0000000123456791 | ORDERS05 | 51 | logistics | COUNTRY_CODE | yes |
| 0000000123456792 | ORDERS05 | 51 | logistics | DELIVERY_DATE | yes |
| 0000000123456793 | ORDERS05 | 51 | manufacturing | MATERIAL_MISSING | yes if master maps |
| 0000000123456794 | ORDERS05 | 51 | manufacturing | UOM_MISMATCH PC→EA | yes |
| 0000000123456795 | ORDERS05 | 51 | manufacturing | PLANT_INVALID | yes/escalate if no plant map |
| 0000000987654321 | INVOIC02 | 64 | finance | none | SKIP (not failed) |
| 0000000987654400 | INVOIC02 | 51 | finance | PO_REFERENCE / amount | HITL strictly |
| 0000000987654401 | INVOIC02 | 51 | finance | VENDOR_COMPANY_CODE | maybe |
| 0000000555000001 | DEBMAS06 | 53 | master_data | none | SKIP success |
| 0000000555000099 | DEBMAS06 | 51 | master_data | INVALID_REFERENCE (ICC) | depends |
| 0000000666000001 | ORDERS05 | 56 | basis | PARTNER_PROFILE | ESCALATE never patch |
| 0000000777000001 | ORDERS05 | 51 | unknown | UNKNOWN / messy dump text | low confidence HITL or escalate |

Error texts are intentionally mixed: some are clean (`Customer CUST-OLD-12345 not found`), some look like dump lines. Your classifier must not assume a single field named `errorCode`.
