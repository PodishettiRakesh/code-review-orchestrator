"""
Stage 4: Run Security Agent after Code Analyzer (no graph).
Usage: from project root or backend/ with GROQ_API_KEY set:
  python backend/run_security.py
"""
import sys
from pathlib import Path

# Ensure backend is on path when run from project root
_backend = Path(__file__).resolve().parent
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

from app import create_initial_state, code_analyzer_node, security_agent_node


def main() -> None:
    snippet = """
import sqlite3
def get_user(name):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = '" + name + "'")
    return cur.fetchone()
"""
    state = create_initial_state(snippet.strip(), "python")
    # Run analyzer first so Security Agent has analysis_notes
    state.update(code_analyzer_node(state))
    result = security_agent_node(state)
    print("--- security_findings ---")
    print(result.get("security_findings", ""))
    print("\nStage 4 OK: Security Agent node ran successfully.")


if __name__ == "__main__":
    main()
