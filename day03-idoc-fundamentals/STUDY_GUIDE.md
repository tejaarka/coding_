# Day 3 — SAP IDoc Fundamentals (Part 1)

**Time:** 2–3 hours
**Goal:** Explain IDoc structure in 3 sentences, and identify key fields in a real IDoc XML.
**Project link:** Electrolux iDoc Self-Heal / SAP ICC POCs on TCS AI AXIS.

This lab is **read-and-parse only**. You do not need SAP GUI, Citrix, or a live SAP system today.

---

## 0. The 3-sentence explanation (memorize this)

1. An **IDoc (Intermediate Document)** is SAP’s standard envelope for sending or receiving a business document such as an order, invoice, or customer master.
2. Every IDoc has a **control record** (who sent it, who should receive it, what type it is, current status), **data segments** (the actual business fields), and **status records** (the processing history / error trail).
3. When SAP cannot post the business document, the IDoc stays in an error status (commonly **51**); that failed envelope is exactly what the Electrolux self-heal AI will read, diagnose, and patch.

If you can say those three sentences without notes, Day 3 is working.

---

## 1. What is SAP, and why it matters here

**SAP** is the ERP (enterprise resource planning) system Electrolux uses to run sales, purchasing, manufacturing, finance, and customer master data.

Think of it as the company’s system of record:

| Business event | Typical SAP module | What SAP stores |
| --- | --- | --- |
| Customer places / company sends an order | SD (Sales & Distribution) | Order header, partners, line items |
| Supplier / intercompany invoice arrives | MM / FI | Invoice amounts, tax, vendor |
| New intercompany customer must exist | SD / FI master data | Customer number, name, company code, sales area |
| Production order / stock movement | PP / MM | Materials, plants, quantities |

SAP does **not** always create those documents by a human typing in a screen. Other SAP systems, EDI partners, and middleware send structured messages. The standard SAP message format for that is the **IDoc**.

### Why this matters for Electrolux / AI AXIS

From the team discussions and the live TCS AI AXIS screens:

- Failed **IDocs** are the raw material of **iDoc Self-Heal**.
- The **SAP ICC** report is automating **intercompany customer creation** (a master-data IDoc flow, typically **DEBMAS**).
- **ABAP Dump Analysis** is a *different* SAP problem (runtime crashes in ST22). Useful later; **not** today’s topic.

Your job on Day 3 is to read the **document envelope** so that later you can write a parser, a diagnostic prompt, and a segment patch.

---

## 2. IDoc architecture — three records, three database tables

Inside SAP, one IDoc is stored across three tables. When the IDoc is exported as XML, you mainly see the first two.

```
+--------------------------------------------------------------+
| CONTROL RECORD  table EDIDC   XML tag: EDI_DC40              |
| "The envelope label"                                         |
| DOCNUM, IDOCTYP, MESTYP, SNDPRN, RCVPRN, DIRECT, STATUS      |
+--------------------------------------------------------------+
| DATA RECORDS    table EDID4   XML tags: E1EDK01, E1EDKA1...  |
| "The letter inside the envelope"                             |
| Hierarchical segments = header / partners / items / totals   |
+--------------------------------------------------------------+
| STATUS RECORDS  table EDIDS   usually NOT in the XML file    |
| "The tracking history"                                       |
| 64 ready -> 51 error -> 53 posted   (with timestamps/messages)|
+--------------------------------------------------------------+
```

### 2.1 Control record (`EDIDC` / `EDI_DC40`)

This is metadata. It does **not** contain the order quantity or customer street address. It answers:

- Which IDoc is this? (`DOCNUM`)
- What business message is it? (`MESTYP` = `ORDERS`, `INVOIC`, `DEBMAS`)
- What technical structure/version is it? (`IDOCTYP` = `ORDERS05`, `INVOIC02`, `DEBMAS06`)
- Who sent it / who should receive it? (`SNDPRN` / `RCVPRN`)
- Is SAP sending or receiving? (`DIRECT`: `1` outbound, `2` inbound)
- Did processing succeed? (`STATUS`)

**Project mapping:** your ingestion service will key incidents off `DOCNUM` + `STATUS` + `MESTYP`.

### 2.2 Data records / segments (`EDID4`)

This is the payload. Segments are named with short SAP codes. Naming pattern for order/invoice IDocs:

| Letters | Meaning | Example |
| --- | --- | --- |
| `E1` | Released external segment | all standard segments |
| `ED` | EDI document | |
| `K` | Kopf = **header** | `E1EDK01` header general |
| `P` | Position = **line item** | `E1EDP01` item general |
| `A` | Address / partner | `E1EDKA1` header partner |
| `S` | Summe = **totals** | `E1EDS01` summary |

Master-data IDocs (customer, material) use table-based names instead:

| Segment | SAP table it mirrors | Business meaning |
| --- | --- | --- |
| `E1KNA1M` | `KNA1` | Customer general data |
| `E1KNB1M` | `KNB1` | Customer company-code (finance) data |
| `E1KNVVM` | `KNVV` | Customer sales-area data |

Segments are **hierarchical**. An item segment `E1EDP01` can contain child segments such as `E1EDP19` (material identifier).

### 2.3 Status records (`EDIDS`)

Every processing step appends a status:

| Status | Meaning | Typical moment |
| --- | --- | --- |
| `01` | IDoc created | just generated |
| `03` | Data passed to port | outbound handoff |
| `12` | Dispatch OK | partner received it |
| `64` | Ready for application | inbound, waiting to post |
| `51` | Application document **not** posted | business validation failed |
| `53` | Application document posted | success |
| `56` | IDoc added with errors | syntax / partner / structure problem |
| `68` | Error — no further processing | parked / will not retry automatically |

**Important:** XML exports usually contain **control + data only**. Status history lives in SAP (`WE02` / `BD87` / table `EDIDS`). For the POC, status often arrives separately from the SAP connector (`STATUS` on the control record is the *current* status).

---

## 3. Control record vs data segments (worked contrast)

From `samples/ORDERS05_failed_status51.xml`:

**Control record (routing + status):**

| Field | Value | Meaning |
| --- | --- | --- |
| `DOCNUM` | `0000000123456789` | Unique IDoc number |
| `MESTYP` | `ORDERS` | This is a sales/purchase **order** |
| `IDOCTYP` | `ORDERS05` | Structure version 05 |
| `DIRECT` | `2` | **Inbound** (SAP is receiving it) |
| `STATUS` | `51` | Failed to post |
| `SNDPRN` | `ELECTROLUX_EU` | Sending logical system |
| `RCVPRN` | `ELECTROLUX_US` | Receiving logical system |

**Data segments (business content):**

| Segment | Field | Value | Business meaning |
| --- | --- | --- | --- |
| `E1EDK01` | `CURCY` | `USD` | Order currency |
| `E1EDKA1` (`PARVW=AG`) | `PARTN` | `CUST-OLD-12345` | Sold-to customer number — **this is the likely failure** |
| `E1EDP01` | `MENGE` | `10.000` | Quantity of line 10 |
| `E1EDP19` | `IDTNR` | `ELX-FRIDGE-900` | Material number |

Self-heal logic later:

1. Read control: inbound `ORDERS` in status `51`.
2. Read payload: sold-to `PARTN = CUST-OLD-12345`.
3. Match historical rule: old customer IDs were migrated to `CUST-NEW-...`.
4. Patch **data segment** `E1EDKA1-PARTN`, **not** the control record.
5. Reprocess (BD87 equivalent) until status becomes `53`.

---

## 4. Message type vs IDoc type vs partner profile

These three names are easy to mix up. They are not the same thing.

```
Message type  MESTYP   = the business intent     ORDERS / INVOIC / DEBMAS
IDoc type     IDOCTYP  = the XML/segment schema  ORDERS05 / INVOIC02 / DEBMAS06
Partner profile WE20   = who is allowed to send/receive that message
```

- `ORDERS` can be carried by basic types `ORDERS01` … `ORDERS05`. Electrolux-style landscapes almost always use the latest common one, **ORDERS05**.
- The **partner profile** (transaction `WE20`) is SAP’s ACL + routing table:
  - partner number (logical system / customer / vendor)
  - partner type (`LS` logical system, `KU` customer, `LI` vendor)
  - inbound or outbound message type
  - which process code / function module posts it
  - optional conversion rules (unit of measure `PC` → `EA`, etc.)

If a partner profile is missing or wrong, the IDoc often fails **before** business validation (status **56** or stuck at **64**), not with a field-level application error (**51**).

**Project mapping:** AI can patch a wrong customer number in `E1EDKA1`. It cannot invent a missing partner profile. That class of failure is configuration, and should be escalated rather than auto-healed.

---

## 5. Inbound vs outbound

`DIRECT` on the control record:

| `DIRECT` | Direction | Who creates the IDoc | Who posts the business document |
| --- | --- | --- | --- |
| `1` | **Outbound** | This SAP system | The partner / the other SAP |
| `2` | **Inbound** | The partner / the other SAP | **This** SAP system |

Electrolux examples:

- EU company code sends a purchase order to US company code → US SAP sees an **inbound ORDERS05**.
- US SAP sends an invoice back → EU SAP sees an **inbound INVOIC02**.
- Intercompany customer master is distributed from a hub → receiving SAP sees an **inbound DEBMAS06**.

**Self-heal almost always targets inbound IDocs.** Outbound failures are usually “could not send” (port, RFC destination, partner). Inbound failures are “SAP refused to post this payload” — that is where segment patches help.

---

## 6. Common IDoc types you will see

### 6.1 `ORDERS05` — sales / purchase order

**Message type:** `ORDERS`
**Typical module:** SD / MM
**Sample:** `samples/ORDERS05_failed_status51.xml`

| Segment | Business meaning |
| --- | --- |
| `EDI_DC40` | Envelope |
| `E1EDK01` | Header: currency, action, document number |
| `E1EDKA1` | Partners (sold-to, ship-to, bill-to) |
| `E1EDK14` | Org data: sales org, division, distribution channel |
| `E1EDK03` | Dates (document date, delivery date) |
| `E1EDP01` | Line item: quantity, unit, price |
| `E1EDP19` | Material identifier on that line |

Frequent status-51 causes: unknown customer, unknown material, invalid plant, unit-of-measure mismatch, missing sales area.

### 6.2 `INVOIC02` — invoice

**Message type:** `INVOIC`
**Typical module:** SD billing / MM invoice verification / FI
**Sample:** `samples/INVOIC02_inbound.xml`

| Segment | Business meaning |
| --- | --- |
| `E1EDK01` | Invoice header, currency, invoice number (`BELNR`) |
| `E1EDKA1` | Bill-from / bill-to partners |
| `E1EDP01` | Invoice line: quantity, amount |
| `E1EDS01` | Totals |

Frequent status-51 causes: PO reference missing, tax code, amount mismatch, vendor not extended to company code.

### 6.3 `DEBMAS06` — customer master

**Message type:** `DEBMAS`
**Typical module:** SD + FI master data
**Sample:** `samples/DEBMAS06_customer_create.xml`

This is the IDoc behind **SAP ICC / intercompany customer creation** on the AI AXIS dashboard.

| Segment | SAP table | Business meaning |
| --- | --- | --- |
| `E1KNA1M` | `KNA1` | General customer: number (`KUNNR`), name, country, account group |
| `E1KNB1M` | `KNB1` | Company-code view (needed for FI posting) |
| `E1KNVVM` | `KNVV` | Sales-area view (needed for orders) |

A customer that exists in `KNA1` but is missing `KNB1` / `KNVV` will cause later `ORDERS05` IDocs to fail with “customer not defined in sales area / company code”. That is why ICC customer creation is a priority use case.

`MSGFN` on DEBMAS segments is the function code, commonly:

| `MSGFN` | Meaning |
| --- | --- |
| `009` | Original / create |
| `004` | Change |
| `005` | Replace / update |

---

## 7. Partner functions you must recognize (`E1EDKA1-PARVW`)

The same segment `E1EDKA1` is repeated once per partner. `PARVW` tells you **which** partner.

| `PARVW` | German origin | English | Typical field for the ID |
| --- | --- | --- | --- |
| `AG` | Auftraggeber | Sold-to | `PARTN` |
| `WE` | Warenempfänger | Ship-to | `PARTN` |
| `RE` | Rechnungsempfänger | Bill-to | `PARTN` |
| `RG` | Regulierer | Payer | `PARTN` |
| `LF` | Lieferant | Vendor | `PARTN` / `LIFNR` |
| `RS` | Rechnungssteller | Invoice issuer | `LIFNR` |

Never read “the partner number” without checking `PARVW`. Sold-to and ship-to are often different customers.

---

## 8. How this maps to TCS AI AXIS / Electrolux

```
Failed IDoc in Electrolux SAP
        |
        v
Connector reads EDIDC + EDID4 (+ EDIDS message)
        |
        v
AI AXIS incident  (e.g. INC0023935 on SAP ICC screen)
        |
        v
Diagnostic agent looks at STATUS, MESTYP, and the failing segment field
        |
        v
Suggested patch  (example: E1EDKA1 PARTN CUST-OLD-12345 -> CUST-NEW-12345)
        |
        v
Human approval on the web UI  (or auto-apply if confidence is high)
        |
        v
Reprocess inbound IDoc  -> STATUS 53
```

Day 3 competency: you can look at the XML and point to **exactly which tag** the agent would patch.

---

## 9. Hands-on (do this now)

### Step 1 — Open the three samples

```
day03-idoc-fundamentals/samples/ORDERS05_failed_status51.xml
day03-idoc-fundamentals/samples/INVOIC02_inbound.xml
day03-idoc-fundamentals/samples/DEBMAS06_customer_create.xml
```

On `ORDERS05_failed_status51.xml`, find by eye:

1. Control record `EDI_DC40`
2. `STATUS` = `51`
3. `DIRECT` = `2`
4. Segment `E1EDKA1` where `PARVW` = `AG`
5. Field `PARTN` = `CUST-OLD-12345`

That sold-to number is the business field a self-heal agent would change.

### Step 2 — Run the parser

From this folder:

```bash
python3 parse_idoc.py samples/ORDERS05_failed_status51.xml
python3 parse_idoc.py samples/INVOIC02_inbound.xml
python3 parse_idoc.py samples/DEBMAS06_customer_create.xml
python3 parse_idoc.py samples/   # parses every XML in the folder
```

Confirm the parser’s “Likely failure field” for the ORDERS05 file points at `E1EDKA1 / PARTN`.

### Step 3 — Manual mapping exercise

Fill this in without looking at the answer key (answers are in `READINESS_QUESTIONS.md`):

| XML location | What business fact is this? |
| --- | --- |
| `EDI_DC40/DOCNUM` | |
| `EDI_DC40/MESTYP` vs `IDOCTYP` | |
| `E1EDKA1[PARVW=WE]/PARTN` | |
| `E1EDP01/MENGE` + `MENEE` | |
| `E1KNA1M/KUNNR` | |

---

## 10. What you do **not** need today

| Skip | Why |
| --- | --- |
| Writing ABAP | You only need to read IDoc XML |
| WE20/WE21 configuration in a live system | Concept only; no SAP GUI yet |
| ALE distribution models, ports, RFC destinations | Day 4 / infrastructure |
| ABAP dumps (`ST22`) | Separate AXIS report |
| LangChain / FastAPI | Later labs consume this parser, they are not required to *understand* IDocs |

---

## 11. Official docs worth opening (optional, 20 min)

- SAP Help: search **“IDoc interface”** / **“Structure of an IDoc”**
- In a real SAP system later: transaction **WE60** (IDoc documentation), **WE02** (display IDoc), **WE30** (IDoc type)
- Segment lists: ORDERS05 / DEBMAS06 field catalogues (search “complete segment list ORDERS05”)

You do not need to memorize every field. You need the **map**: control vs data vs status, header vs item vs partner, inbound vs outbound.
