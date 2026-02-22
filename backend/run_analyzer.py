"""
Stage 3: Run Code Analyzer agent in isolation (no graph).
Usage: from project root or backend/ with GROQ_API_KEY set:
  python backend/run_analyzer.py
"""
import sys
from pathlib import Path

# Ensure backend is on path when run from project root
_backend = Path(__file__).resolve().parent
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

from app import create_initial_state, code_analyzer_node


def main() -> None:
    snippet = """
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
"""
    state = create_initial_state(snippet.strip(), "python")
    result = code_analyzer_node(state)
    print("--- analysis_notes ---")
    print(result.get("analysis_notes", ""))
    print("\nStage 3 OK: Code Analyzer node ran successfully.")


if __name__ == "__main__":
    main()
