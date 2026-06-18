# AI Multi-Agent Code Review Orchestrator

Multi-agent AI system for structured code reviews using specialized agents and shared state. Each agent focuses on one concern—code quality, security, or performance—and an aggregator synthesizes the results into a structured JSON report.

> **Problem**: Single-prompt LLM reviews mix concerns, dilute context, and produce inconsistent output.  
> **Approach**: Specialized agents with scoped prompts, shared state, and structured aggregation.

## Architecture

Instead of one prompt asking an LLM to review quality, security, and performance together, the pipeline decomposes work into focused agents:

```
┌─────────────────────────────────────────────────────────────┐
│ INPUT: code snippet (+ optional language)                    │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ CODE ANALYZER  → Readability, structure, complexity         │
└────────────┬────────────────────────────────────────────────┘
             │  ReviewState.analysis_notes
             ▼
┌─────────────────────────────────────────────────────────────┐
│ SECURITY AGENT → Injection, secrets, validation, auth risks │
└────────────┬────────────────────────────────────────────────┘
             │  ReviewState.security_findings
             ▼
┌─────────────────────────────────────────────────────────────┐
│ PERFORMANCE AGENT → Loops, memory, I/O, algorithmic issues  │
└────────────┬────────────────────────────────────────────────┘
             │  ReviewState.performance_issues
             ▼
┌─────────────────────────────────────────────────────────────┐
│ AGGREGATOR AGENT → Structured JSON report with severity     │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
        ReviewState.final_report
```

| Aspect | Single prompt | Multi-agent |
|--------|---------------|-------------|
| Focus | Mixed concerns | One concern per agent |
| Testability | Hard to isolate failures | Each node runnable on its own |
| Extensibility | Prompt grows over time | New agents plug into the graph |
| State | Implicit context | Explicit `ReviewState` fields |

Agents are implemented as LangGraph-compatible nodes. Stages 1–6 invoke them sequentially; Stage 7 will wire them into a `StateGraph`.

## Technology Stack

### Implemented

- **Python 3.10+**
- **LangChain** + **langchain-groq** — LLM integration (Groq default)
- **LangGraph** — in dependencies; workflow graph pending (Stage 7)
- **python-dotenv** — environment configuration

### Planned

- **FastAPI** + **Uvicorn** — REST API (Stage 8)
- **React** — analysis UI (Stage 9)

## Implementation Status

| Stage | Component | Status |
|-------|-----------|--------|
| 1 | LLM integration (Groq) | Complete |
| 2 | Shared `ReviewState` schema | Complete |
| 3 | Code Analyzer agent | Complete |
| 4 | Security agent | Complete |
| 5 | Performance agent | Complete |
| 6 | Aggregator agent | Complete |
| 7 | LangGraph `StateGraph` | Next |
| 8 | FastAPI `POST /analyze` | Next |
| 9 | React dashboard | Next |

## Project Structure

```
code-review-orchestrator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── llm.py                   # Groq LLM factory
│   │   ├── state.py                 # ReviewState (TypedDict)
│   │   └── agents/
│   │       ├── code_analyzer.py
│   │       ├── security_agent.py
│   │       ├── performance_agent.py
│   │       └── aggregator_agent.py
│   ├── verify_llm.py                # Stage 1 smoke test
│   ├── run_analyzer.py              # Code Analyzer only
│   ├── run_security.py              # Analyzer → Security
│   ├── run_performance.py           # Analyzer → Performance
│   ├── run_aggregator.py            # Full pipeline (Stages 3–6)
│   └── requirements.txt
├── .env.example
├── .gitignore
├── ProblemSTatement.txt
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+
- Groq API key — [console.groq.com/keys](https://console.groq.com/keys)

### Installation

```bash
git clone <repository-url>
cd code-review-orchestrator

python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r backend/requirements.txt

cp .env.example .env
# Add GROQ_API_KEY to .env

python backend/verify_llm.py
```

### Run the pipeline

```bash
# Full review (Analyzer → Security → Performance → Aggregator)
python backend/run_aggregator.py

# Individual agents
python backend/run_analyzer.py
python backend/run_security.py
python backend/run_performance.py
```

### Example output

```json
{
  "summary": "Well-structured code with minor security concerns.",
  "code_quality": {
    "severity": "low",
    "findings": "Function naming is clear, but missing docstrings."
  },
  "security": {
    "severity": "high",
    "findings": "SQL query concatenation detected. Use parameterized queries."
  },
  "performance": {
    "severity": "medium",
    "findings": "Nested loop may cause unnecessary work on large inputs."
  }
}
```

## Configuration

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant   # optional
```

Supported Groq models: `llama-3.1-8b-instant` (default), `llama-3.3-70b-versatile`, `mixtral-8x7b-32768`.

## ReviewState

All agents read from and write to shared state:

```python
class ReviewState(TypedDict, total=False):
    code_input: str           # Set by caller
    language: str             # Optional hint (e.g. "python")
    analysis_notes: str       # Written by Code Analyzer
    security_findings: str    # Written by Security Agent
    performance_issues: str   # Written by Performance Agent
    final_report: str         # Written by Aggregator (JSON string)
```

| Field | Set by | Description |
|-------|--------|-------------|
| `code_input` | Caller | Code snippet to review |
| `language` | Caller | Optional language hint |
| `analysis_notes` | Code Analyzer | Structure, readability, complexity |
| `security_findings` | Security Agent | Injection, secrets, validation |
| `performance_issues` | Performance Agent | Loops, memory, blocking, complexity |
| `final_report` | Aggregator | JSON with `summary` and per-category severity |

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Multi-agent | Scoped prompts reduce mixed or unfocused findings |
| LangGraph | Deterministic orchestration and explicit state flow |
| Groq default | Fast inference and a usable free tier for development |
| JSON output | Structured, parseable reports for API and UI consumers |
| TypedDict state | Lightweight shared schema, LangGraph-ready |

## Roadmap

1. **Stage 7** — Wire nodes into a LangGraph `StateGraph` with `graph.invoke()`
2. **Stage 8** — FastAPI `POST /analyze` accepting code and optional language
3. **Stage 9** — React dashboard for submission and report display

Future: parallel agent execution, GitHub integration, Redis persistence, Ollama support, additional agents (docs, testing).

## License

Portfolio demonstration for AI automation engineering. Stages 1–6 are complete; Stages 7–9 are in progress.
