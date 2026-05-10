# 🤖 Autonomous Self-Healing DevOps Agent

An automated error-to-production pipeline built with **LangGraph**, **LangChain**, and **FastAPI**.  
A Sentry error triggers a chain of AI agents that create a Notion ticket, write a code fix, open a GitHub PR, review it (with a self-healing loop), get human approval, and deploy — all automatically.

---

## Architecture

```
Sentry Webhook
     │
     ▼
[A1] Notion Agent          → Creates a ticket in Notion
     │
     ▼
[A2] Coder Agent (SE1)     → LLM generates fix → creates branch + PR on GitHub
     │
     ▼
[A3] Code Reviewer (Lead)  → LLM reviews PR diff
     │          │
     │  comments │ approved
     │◄──────────┘          └─────────────────────────────────────┐
     │                                                             │
     ▼                                                             │
[A4] Expectation Reviewer  ◄── ⏸ HUMAN APPROVAL (manager)        │
     │                                                             │
     ▼                                                             │
[A5] QA Agent              → Merges PR + deploys to DEV via GH Actions
     │
     ▼
[A6] Infra Agent           ◄── ⏸ HUMAN APPROVAL (ops) → deploys to PROD
     │
     ▼
   END
```

---

## Project Structure

```
├── agents/
│   ├── notion_agent.py       # A1 – Creates Notion ticket
│   ├── coder_agent.py        # A2 – LLM code fix + GitHub PR
│   ├── reviewer_agent.py     # A3 – LLM PR review (loop-aware)
│   ├── expectation_agent.py  # A4 – Manager approval (human-in-the-loop)
│   ├── qa_agent.py           # A5 – DEV/TEST deployment
│   └── infra_agent.py        # A6 – PROD deployment (human-in-the-loop)
├── graph/
│   ├── state.py              # AgentState TypedDict
│   └── builder.py            # StateGraph construction & compilation
├── tools/
│   ├── notion_tools.py       # Notion API stubs (fill credentials)
│   └── github_tools.py       # GitHub API stubs (fill credentials)
├── utils/
│   └── llm_factory.py        # OpenAI / Anthropic factory (cached)
├── config/
│   └── settings.py           # All config from environment variables
├── webhook_server.py          # FastAPI webhook receiver
├── main.py                    # CLI demo runner
├── requirements.txt
└── .env.example               # Template — copy to .env and fill in
```

---

## Quickstart

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

> **Keys needed to get started:**
> - `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`)
> - `NOTION_API_KEY` + `NOTION_DATABASE_ID`
> - `GITHUB_TOKEN` + `GITHUB_REPO`

### 3. Run locally (CLI demo with placeholder tools)

```bash
python main.py
```

The pipeline runs through all nodes using placeholder Notion/GitHub stubs.  
You will be prompted twice for human approval (A4 and A6).

### 4. Run the webhook server

```bash
uvicorn webhook_server:app --reload --port 8000
```

Point your Sentry webhook to: `http://your-server:8000/webhook/sentry`

---

## Filling in Real Credentials

### Notion
1. Create a Notion Integration at https://www.notion.so/my-integrations
2. Share your database with the integration
3. Set `NOTION_API_KEY` and `NOTION_DATABASE_ID` in `.env`
4. Uncomment `notion-client` in `requirements.txt` and `pip install notion-client`
5. Replace the `# TODO` blocks in `tools/notion_tools.py`

### GitHub
1. Create a Personal Access Token with `repo` + `workflow` scopes
2. Set `GITHUB_TOKEN` and `GITHUB_REPO` in `.env`
3. Uncomment `PyGithub` in `requirements.txt` and `pip install PyGithub`
4. Replace the `# TODO` blocks in `tools/github_tools.py`

---

## Human-in-the-Loop

The graph pauses **before** two nodes (`interrupt_before`):

| Node | Who approves | What to check |
|------|-------------|---------------|
| `expectation_agent` (A4) | Manager / Product Owner | Notion ticket vs PR alignment |
| `infra_agent` (A6) | Ops / SRE | DEV test results before PROD deploy |

**Via CLI:** The `main.py` prompts you to press ENTER.

**Via API (webhook server):**
```bash
# Approve A4 (expectation check)
curl -X POST http://localhost:8000/resume/{thread_id} \
     -H "Content-Type: application/json" \
     -d '{"expectation_approved": true}'

# Approve A6 (PROD deploy) — no body needed
curl -X POST http://localhost:8000/resume/{thread_id} \
     -H "Content-Type: application/json" \
     -d '{}'
```

---

## Switching LLM Providers

Set in `.env`:

```env
# OpenAI (default)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o

# Anthropic
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
```

---

## Production Checklist

- [ ] Replace `MemorySaver` with `SqliteSaver` or `RedisSaver` in `graph/builder.py`
- [ ] Fill in `tools/notion_tools.py` with real Notion SDK calls
- [ ] Fill in `tools/github_tools.py` with real PyGithub calls
- [ ] Update `QA_WORKFLOW_FILE` and `PROD_WORKFLOW_FILE` in agent files
- [ ] Set `WEBHOOK_SECRET` to a strong random value
- [ ] Deploy behind HTTPS (Nginx / Cloudflare Tunnel)
- [ ] Add retry logic and alerting for failed deployments
