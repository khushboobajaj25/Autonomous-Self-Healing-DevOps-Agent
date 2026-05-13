"""
config/settings.py
Central config — load from environment variables or a .env file.
Fill in your real credentials in a .env file (never commit it).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ────────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")   # "openai" | "anthropic"
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o")

# ── Sentry ──────────────────────────────────────────────────────────────────
SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
SENTRY_AUTH_TOKEN: str = os.getenv("SENTRY_AUTH_TOKEN", "")
SENTRY_ORG: str = os.getenv("SENTRY_ORG", "")
SENTRY_PROJECT: str = os.getenv("SENTRY_PROJECT", "")

# ── Notion ──────────────────────────────────────────────────────────────────
NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID", "")

# ── GitHub ──────────────────────────────────────────────────────────────────
GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO: str = os.getenv("GITHUB_REPO", "owner/repo")   # e.g. "acme/backend"
GITHUB_BASE_BRANCH: str = os.getenv("GITHUB_BASE_BRANCH", "main")

# ── FastAPI webhook server ──────────────────────────────────────────────────
WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", "8000"))
WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "changeme")
