"""
Stage 5: Performance Agent.
Reads code_input and analysis_notes from state, calls Groq, returns performance_issues.
Focus: nested loops, memory inefficiency, blocking calls, algorithmic complexity.
"""
from app.llm import get_llm
from app.state import ReviewState

PERFORMANCE_AGENT_PROMPT = """You are a performance-focused code reviewer. Analyze the following code for:
- Nested loops and unnecessary iteration
- Memory inefficiency (e.g. large copies, unbounded growth, redundant allocations)
- Blocking or synchronous calls that could block the event loop or threads
- Algorithmic complexity (e.g. O(n^2) where O(n) is possible, inefficient data structures)

Use the prior analysis notes below only for context; focus your output on performance findings only.
Provide concise, actionable performance notes. Do not repeat the code.

Prior analysis notes (for context):
{analysis_notes}

Code:
{code}
"""

PERFORMANCE_AGENT_PROMPT_WITH_LANGUAGE = """You are a performance-focused code reviewer. Analyze the following {language} code for:
- Nested loops and unnecessary iteration
- Memory inefficiency (e.g. large copies, unbounded growth, redundant allocations)
- Blocking or synchronous calls that could block the event loop or threads
- Algorithmic complexity (e.g. O(n^2) where O(n) is possible, inefficient data structures)

Use the prior analysis notes below only for context; focus your output on performance findings only.
Provide concise, actionable performance notes. Do not repeat the code.

Prior analysis notes (for context):
{analysis_notes}

Code:
{code}
"""


def performance_agent_node(state: ReviewState) -> dict:
    """
    LangGraph node: read code_input and analysis_notes, call LLM, return partial state with performance_issues.
    """
    code_input = state["code_input"]
    analysis_notes = state.get("analysis_notes") or ""
    language = state.get("language") or ""

    if language:
        prompt = PERFORMANCE_AGENT_PROMPT_WITH_LANGUAGE.format(
            language=language, analysis_notes=analysis_notes or "(none)", code=code_input
        )
    else:
        prompt = PERFORMANCE_AGENT_PROMPT.format(
            analysis_notes=analysis_notes or "(none)", code=code_input
        )

    llm = get_llm()
    response = llm.invoke(prompt)
    return {"performance_issues": response.content}
