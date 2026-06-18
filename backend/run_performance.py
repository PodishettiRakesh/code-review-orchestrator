"""
Stage 5: Run Performance Agent after Code Analyzer (no graph).
Usage: from project root or backend/ with GROQ_API_KEY set:
  python backend/run_performance.py
"""
import sys
from pathlib import Path

# Ensure backend is on path when run from project root
_backend = Path(__file__).resolve().parent
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

from app import create_initial_state, code_analyzer_node, performance_agent_node


def main() -> None:
    snippet = """
def process_items(items):
    result = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j:
                result.append(items[i] + items[j])
    return result
"""
    state = create_initial_state(snippet.strip(), "python")
    # Run analyzer first so Performance Agent has analysis_notes
    state.update(code_analyzer_node(state))
    result = performance_agent_node(state)
    print("--- performance_issues ---")
    print(result.get("performance_issues", ""))
    print("\nStage 5 OK: Performance Agent node ran successfully.")


if __name__ == "__main__":
    main()
