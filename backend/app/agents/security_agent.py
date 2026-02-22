"""
Stage 4: Security Agent.
Reads code_input and analysis_notes from state, calls Groq, returns security_findings.
Focus: injection risks, hardcoded secrets, input validation issues.
"""
from app.llm import get_llm
from app.state import ReviewState

SECURITY_AGENT_PROMPT = """You are a security-focused code reviewer. Analyze the following code for:
- Injection risks (SQL, command, OS, or other injection)
- Hardcoded secrets, credentials, API keys, or sensitive data
- Input validation issues (missing or weak validation, unsafe use of user input)

Use the prior analysis notes below only for context; focus your output on security findings only.
Provide concise, actionable security notes. Do not repeat the code.

Prior analysis notes (for context):
{analysis_notes}

Code:
{code}
"""

SECURITY_AGENT_PROMPT_WITH_LANGUAGE = """You are a security-focused code reviewer. Analyze the following {language} code for:
- Injection risks (SQL, command, OS, or other injection)
- Hardcoded secrets, credentials, API keys, or sensitive data
- Input validation issues (missing or weak validation, unsafe use of user input)

Use the prior analysis notes below only for context; focus your output on security findings only.
Provide concise, actionable security notes. Do not repeat the code.

Prior analysis notes (for context):
{analysis_notes}

Code:
{code}
"""


def security_agent_node(state: ReviewState) -> dict:
    """
    LangGraph node: read code_input and analysis_notes, call LLM, return partial state with security_findings.
    """
    code_input = state["code_input"]
    analysis_notes = state.get("analysis_notes") or ""
    language = state.get("language") or ""

    if language:
        prompt = SECURITY_AGENT_PROMPT_WITH_LANGUAGE.format(
            language=language, analysis_notes=analysis_notes or "(none)", code=code_input
        )
    else:
        prompt = SECURITY_AGENT_PROMPT.format(
            analysis_notes=analysis_notes or "(none)", code=code_input
        )

    llm = get_llm()
    response = llm.invoke(prompt)
    return {"security_findings": response.content}
