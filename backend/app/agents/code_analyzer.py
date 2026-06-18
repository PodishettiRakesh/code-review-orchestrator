"""
Stage 3: Code Analyzer agent.
Reads code_input (and optional language) from state, calls Groq, returns analysis_notes.
"""
from app.llm import get_llm
from app.state import ReviewState

CODE_ANALYZER_PROMPT = """You are a senior code reviewer. Analyze the following code for:
- Structure and organization
- Readability and maintainability
- Complexity (cyclomatic complexity, nesting, unclear logic)
- Risky or error-prone patterns

Provide concise, actionable notes. Do not repeat the code; focus on findings and recommendations.

Code:
{code}
"""

CODE_ANALYZER_PROMPT_WITH_LANGUAGE = """You are a senior code reviewer. Analyze the following {language} code for:
- Structure and organization
- Readability and maintainability
- Complexity (cyclomatic complexity, nesting, unclear logic)
- Risky or error-prone patterns

Provide concise, actionable notes. Do not repeat the code; focus on findings and recommendations.

Code:
{code}
"""


def code_analyzer_node(state: ReviewState) -> dict:
    """
    LangGraph node: read code_input (and optional language), call LLM, return partial state with analysis_notes.
    """
    code_input = state["code_input"]
    language = state.get("language") or ""

    if language:
        prompt = CODE_ANALYZER_PROMPT_WITH_LANGUAGE.format(language=language, code=code_input)
    else:
        prompt = CODE_ANALYZER_PROMPT.format(code=code_input)

    llm = get_llm()
    response = llm.invoke(prompt)
    return {"analysis_notes": response.content}
