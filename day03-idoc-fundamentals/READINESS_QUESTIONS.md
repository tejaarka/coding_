# Day 3 readiness questions

Answer in writing (or out loud as if Arka asked). Then check the answer key at the bottom. Do not memorize ABAP. You are ready when you can point at XML tags and explain the envelope.

---

## A. Explain in 3 sentences (required)

Write your answer, then compare.

1. What is an IDoc?
2. What are the three parts of an IDoc?
3. What does status 51 mean for Electrolux self-heal?

---

## B. Short answer

**B1.** SAP is used at Electrolux as _______. An IDoc is how SAP _______ a business document with another system.

**B2.** Match the SAP table to the IDoc part:

| Table | Part |
| --- | --- |
| EDIDC | |
| EDID4 | |
| EDIDS | |

**B3.** In XML, the control record tag is _______. The sold-to partner lives in segment _______ with `PARVW` = _______.

**B4.** Difference between `MESTYP=ORDERS` and `IDOCTYP=ORDERS05`?

**B5.** `DIRECT=2` means _______. Self-heal usually targets _______ IDocs because _______.

**B6.** Partner profile (WE20) answers which question: (a) what is the order quantity, (b) is this sender allowed to send this message type to this receiver, (c) what is the customer street?

**B7.** Name one typical payload for each:

| IDoc type | Business document |
| --- | --- |
| ORDERS05 | |
| INVOIC02 | |
| DEBMAS06 | |

**B8.** Why can a successful `DEBMAS06` still be a prerequisite for fixing a failed `ORDERS05`?

**B9.** Status 56 vs status 51 — which one is a better candidate for an AI **segment patch**, and why?

**B10.** `E1EDK01` vs `E1EDP01` vs `E1EDKA1` — header, item, or partner?

---

## C. Read the real XML (closed-book, open file)

Open `samples/ORDERS05_failed_status51.xml`.

**C1.** IDoc number (`DOCNUM`)?
**C2.** Inbound or outbound?
**C3.** Current status, in words?
**C4.** Sender logical system?
**C5.** Sold-to number and name?
**C6.** Ship-to number?
**C7.** Material on item 000010?
**C8.** Quantity and unit on item 000020?
**C9.** If you were writing a self-heal patch, which **segment + field** would you change first, and to what kind of value?
**C10.** Would you change `EDI_DC40/STATUS` in the XML to “fix” it? Why or why not?

Open `samples/DEBMAS06_customer_create.xml`.

**C11.** What customer number is being created?
**C12.** Which segment is company-code data? Which is sales-area data?
**C13.** `MSGFN=009` means?
**C14.** Status is 53. Is this a failed IDoc?
**C15.** How does this file relate to the AI AXIS “SAP ICC / Intercompany customer creation” screen?

---

## D. Scenario questions (project thinking)

**D1.** An inbound ORDERS05 is status 64 for 6 hours. Is that a self-heal case?

**D2.** Two `E1EDKA1` segments exist, `AG` and `WE`, with different `PARTN` values. The error text says “ship-to party not found”. Which field do you patch?

**D3.** Electrolux US cannot create customer `0006000521` (“Invalid reference ID”). Is that more likely ORDERS05 or DEBMAS06? Which AXIS report would show the ticket?

**D4.** The LLM suggests changing `MENEE` from `PC` to `EA` because of a known unit mapping. Which layer is that (control, data, status)? Is it a reasonable auto-heal if a partner-profile conversion already exists?

**D5.** You can explain the architecture but cannot find `E1EDKA1` in a new IDoc type `MATMAS05`. What do you do instead of guessing?

---

## E. Teammate drill (say this out loud)

Practice until this is natural:

> “An IDoc is SAP’s envelope for a business document. The control record tells us number, type, sender, receiver, direction, and status. The data segments are the actual header, partners, and items. Status 51 means SAP rejected the application posting, so our agent reads the failing segment — for example sold-to `E1EDKA1-PARTN` — proposes a patch, and we reprocess. Status 56 is usually partner-profile/config, not a field patch. DEBMAS06 is customer master; if ICC customer create fails, later ORDERS IDocs will fail too.”

---

# Answer key

## A

1. An IDoc is SAP’s standard structured message for exchanging a business document (order, invoice, customer master, etc.) with another SAP or external system.
2. Control record (EDIDC / EDI_DC40), data segments (EDID4 / E1…), status records (EDIDS, processing history).
3. Status 51 means the inbound document was received but SAP did **not** post it (application error). That failed payload is what self-heal diagnoses and patches.

## B

**B1.** system of record / ERP; sends or receives (exchanges)
**B2.** EDIDC = control; EDID4 = data segments; EDIDS = status history
**B3.** `EDI_DC40`; `E1EDKA1`; `AG`
**B4.** Message type = business intent (an order). IDoc type = concrete segment schema/version (ORDERS05).
**B5.** Inbound; inbound; because this SAP is the one refusing to post, so a payload patch + reprocess can succeed.
**B6.** (b)
**B7.** ORDERS05 = sales/purchase order; INVOIC02 = invoice; DEBMAS06 = customer master
**B8.** ORDERS posting needs the customer to exist (and be extended to company code + sales area). DEBMAS creates/extends that master. ICC create failures show up as later order IDoc 51s.
**B9.** 51 — application/field/master-data mismatch. 56 is typically structure or partner-profile setup.
**B10.** `E1EDK01` header; `E1EDP01` item; `E1EDKA1` partner

## C

**C1.** `0000000123456789`
**C2.** Inbound (`DIRECT=2`)
**C3.** 51 — application document not posted
**C4.** `ELECTROLUX_EU`
**C5.** `CUST-OLD-12345` / Electrolux EU Intercompany Sold-To
**C6.** `0006000521`
**C7.** `ELX-FRIDGE-900`
**C8.** `5.000` `EA`
**C9.** `E1EDKA1` where `PARVW=AG`, field `PARTN`, map `CUST-OLD-12345` to the post-migration customer number (also check bill-to `RE`, which uses the same old id)
**C10.** No. Status is a **result** of posting, not a field you edit to fake success. Change the business data, then reprocess so SAP sets status 53 itself.
**C11.** `0006000521`
**C12.** `E1KNB1M` company code; `E1KNVVM` sales area
**C13.** Original / create
**C14.** No — 53 is posted successfully
**C15.** ICC automates intercompany customer creation; a successful DEBMAS06 is the SAP document behind a Success incident like “customer 0006000521 is…”

## D

**D1.** Not yet. 64 = waiting to post. Check inbound processing / job, not a field patch.
**D2.** `E1EDKA1` with `PARVW=WE`, field `PARTN` (ship-to), not the sold-to.
**D3.** DEBMAS (customer master) / SAP ICC report, not the ORDERS self-heal path.
**D4.** Data segment (`E1EDP01-MENEE`). Reasonable if historical mapping exists **and** SAP still rejects `PC`. If WE20 already converts UoM, the real bug may be elsewhere — verify before auto-applying.
**D5.** Look up the basic type in WE60 / segment catalogue. Material master uses `E1MARAM` etc., not `E1EDKA1`. Unmapped segments stay “unknown until documented”; do not invent mappings.

---

## Ready-up bar (tick before Day 4)

- [ ] I can give the 3-sentence IDoc explanation without notes
- [ ] I can mark control vs data vs status on a printed XML
- [ ] I can tell inbound from outbound using `DIRECT`
- [ ] I can tell message type from IDoc type
- [ ] I can find sold-to vs ship-to using `PARVW`
- [ ] I know 51 vs 53 vs 56 vs 64 in one line each
- [ ] I know ORDERS05 / INVOIC02 / DEBMAS06 business meaning
- [ ] I ran `python3 parse_idoc.py samples/` successfully
- [ ] I can point at the field a self-heal agent would patch in the failed ORDERS05 sample
