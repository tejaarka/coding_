# Day 3 — SAP IDoc Fundamentals

Hands-on lab for Electrolux / TCS AI AXIS onboarding.

| File | What to do |
| --- | --- |
| [STUDY_GUIDE.md](STUDY_GUIDE.md) | Read first (explanations + mapping) |
| [samples/](samples/) | Real-shaped IDoc XML (ORDERS05, INVOIC02, DEBMAS06) |
| [parse_idoc.py](parse_idoc.py) | Parse a file and print control / segments / heal hint |
| [READINESS_QUESTIONS.md](READINESS_QUESTIONS.md) | Closed-book questions + answer key |

```bash
python3 parse_idoc.py samples/ORDERS05_failed_status51.xml
python3 parse_idoc.py samples/
```

No extra Python packages required (stdlib `xml.etree.ElementTree` only).
