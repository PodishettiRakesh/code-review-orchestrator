"""
Stage 2: Shared state schema for the code review pipeline.
Each LangGraph agent reads and updates this state.
"""
from typing import TypedDict


class ReviewState(TypedDict, total=False):
    """Shared state for the code review pipeline. Each agent reads and updates this."""

    # Set at pipeline start (API / invoke). Read by: Analyzer, Security, Performance.
    code_input: str
    # Optional; set at start. Read by: agents for context (e.g. Stage 8 POST /analyze).
    language: str
    # Written by: Code Analyzer (Stage 3). Read by: Security, Performance, Aggregator.
    analysis_notes: str
    # Written by: Security Agent (Stage 4). Read by: Aggregator.
    security_findings: str
    # Written by: Performance Agent (Stage 5). Read by: Aggregator.
    performance_issues: str
    # Written by: Aggregator Agent (Stage 6). Read by: API response.
    final_report: str


def create_initial_state(code_input: str, language: str = "") -> dict:
    """Build initial state for graph.invoke(). Only code_input (and optional language) set."""
    state: dict = {"code_input": code_input}
    if language:
        state["language"] = language
    return state
