"""
Stage 6: Aggregator Agent.
Reads analysis_notes, security_findings, performance_issues from state; produces
structured JSON report with summary and categorized severity; stores final_report.
"""
from app.llm import get_llm
from app.state import ReviewState

AGGREGATOR_PROMPT = """You are a code review summarizer. Combine the following three review sections into a single JSON report.

Requirements:
- Output only valid JSON. No markdown, no code fences, no explanation outside the JSON.
- Include a short "summary" (2-3 sentences) summarizing the overall review.
- Include three sections: "code_quality", "security", "performance".
- Each section must have "severity" (one of: "high", "medium", "low") and "findings" (string with the relevant findings).
- Use the exact keys: summary, code_quality, security, performance. Each of the three sections has severity and findings.

Example shape:
{{"summary": "...", "code_quality": {{"severity": "medium", "findings": "..."}}, "security": {{"severity": "high", "findings": "..."}}, "performance": {{"severity": "low", "findings": "..."}}}}

Code quality (structure, readability, complexity):
{analysis_notes}

Security findings:
{security_findings}

Performance issues:
{performance_issues}
"""


def aggregator_agent_node(state: ReviewState) -> dict:
    """
    LangGraph node: read analysis_notes, security_findings, performance_issues;
    call LLM to produce structured JSON; return partial state with final_report.
    """
    analysis_notes = state.get("analysis_notes") or ""
    security_findings = state.get("security_findings") or ""
    performance_issues = state.get("performance_issues") or ""

    prompt = AGGREGATOR_PROMPT.format(
        analysis_notes=analysis_notes or "(none)",
        security_findings=security_findings or "(none)",
        performance_issues=performance_issues or "(none)",
    )

    llm = get_llm()
    response = llm.invoke(prompt)
    content = response.content.strip()
    # Strip markdown code fence if present so final_report is plain JSON
    if content.startswith("```"):
        lines = content.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)
    return {"final_report": content}
