# Install before you write code

Install **only what is definitely needed** for this mock. Everything else waits.

## Definitely needed

| Tool | Why this project needs it | Install |
| --- | --- | --- |
| **Git** | You version the project | Already on most machines. Check: `git --version` |
| **Python 3.11 or 3.12** | All mock services and agents | [python.org](https://www.python.org/downloads/) or `pyenv`. Check: `python3 --version` |
| **pip** | Install libraries | Comes with Python. Check: `python3 -m pip --version` |
| **VS Code** (or any editor) | Edit templates | You already use Cursor/VS Code |
| **A terminal** | Run mock SAP + orchestrator | Built-in |

Create a virtualenv **inside this folder** (you run these):

```bash
cd idoc_selfheal_mock
python3 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Libraries in `requirements.txt` (required)

| Library | Why |
| --- | --- |
| **fastapi** | Mock **SAP endpoints** (failed IDocs, master lookup, reprocess) — stands in for Electrolux APIs |
| **uvicorn** | Runs FastAPI |
| **httpx** | Agents/tools **call** those APIs (endpoint tools + code tools) |
| **pydantic** | Structured payloads: IDoc summary, category, patch, approval — same idea as “structured LLM output” later |
| **python-dotenv** | Config (`SAP_BASE_URL`, later API keys) without hardcoding |

That is enough to touch: REST, JSON, polling, tool types, orchestrator, HITL (CLI).

## Do **not** install yet (not definite)

| Tool | Why wait |
| --- | --- |
| LangChain / LlamaIndex | Orchestrator can be plain Python first; LLM is optional layer |
| OpenAI / Azure OpenAI SDK | Needs a key + cost; classify with **rules** first, then optionally LLM |
| MCP SDK | MCP is a **server** to host tools; Electrolux may not give it |
| Azure Cosmos / Service Bus SDKs | Environment not confirmed |
| PyRFC / SAP NW RFC SDK | Team said call **their HTTP APIs**, not deep RFC |
| Docker / Kubernetes | Nice later; not needed to learn the use case |
| React / Streamlit | HITL can be **CLI** first; UI after the flow works |
| pytest | Add when you start tests (listed in optional extra) |

Optional later line (do not run until Step 8+):

```bash
python -m pip install pytest openai
```

## Sanity check after install

```bash
python -c "import fastapi, uvicorn, httpx, pydantic, dotenv; print('ok')"
```

If this prints `ok`, stop installing and go to [02_PLAN.md](02_PLAN.md).
