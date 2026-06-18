"""
Stage 6: Run full chain (Analyzer → Security → Performance → Aggregator) without graph.
Usage: from project root or backend/ with GROQ_API_KEY set:
  python backend/run_aggregator.py
"""
import json
import sys
from pathlib import Path

# Ensure backend is on path when run from project root
_backend = Path(__file__).resolve().parent
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

from app import (
    create_initial_state,
    code_analyzer_node,
    security_agent_node,
    performance_agent_node,
    aggregator_agent_node,
)


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
    state.update(code_analyzer_node(state))
    state.update(security_agent_node(state))
    state.update(performance_agent_node(state))
    result = aggregator_agent_node(state)
    final_report = result.get("final_report", "")
    print("--- final_report ---")
    print(final_report)
    try:
        json.loads(final_report)
        print("\n(Valid JSON)")
    except json.JSONDecodeError:
        print("\n(Warning: output is not valid JSON)")
    print("\nStage 6 OK: Aggregator Agent ran successfully.")


if __name__ == "__main__":
    main()
