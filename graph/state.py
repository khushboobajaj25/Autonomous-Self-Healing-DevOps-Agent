"""
graph/state.py
Defines the shared AgentState TypedDict that flows through every node.
"""
from __future__ import annotations

from typing import Annotated, Optional
from typing_extensions import TypedDict
import operator


class AgentState(TypedDict):
    # ── Input ──────────────────────────────────────────────────────────────
    error_log: str                        # Raw Sentry error payload (JSON string)

    # ── A1 – Notion ────────────────────────────────────────────────────────
    notion_url: Optional[str]             # URL of the created Notion ticket
    notion_ticket_id: Optional[str]       # Notion page/ticket ID

    # ── A2 – Coder ─────────────────────────────────────────────────────────
    branch_name: Optional[str]            # Git branch created for the fix
    pr_id: Optional[int]                  # GitHub Pull Request number
    pr_url: Optional[str]                 # GitHub Pull Request URL
    pr_diff: Optional[str]               # Diff content returned for review

    # ── A3 – Code Reviewer ─────────────────────────────────────────────────
    review_comments: Annotated[list[str], operator.add]   # accumulated comments
    review_cycle: int                     # how many review loops have occurred

    # ── A4 – Expectation Reviewer (human-in-the-loop) ──────────────────────
    expectation_approved: Optional[bool]  # True when manager approves

    # ── A5 – QA / Dev Deploy ───────────────────────────────────────────────
    dev_deployment_status: Optional[str]  # "success" | "failed"

    # ── A6 – Infra / Prod Deploy (human-in-the-loop) ───────────────────────
    prod_deployment_status: Optional[str] # "success" | "failed"

    # ── Metadata ───────────────────────────────────────────────────────────
    iteration: int                        # total graph iterations (safety guard)
