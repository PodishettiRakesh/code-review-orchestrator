# AI Multi-Agent Code Review Orchestrator

Multi-agent AI system for structured code reviews using LangGraph orchestration. Uses **Groq** for the LLM (free tier, generous limits). (Stages 1–2: environment and state schema.)

## Setup

1. Create a virtual environment and install dependencies (see backend/).
2. Copy `.env.example` to `.env` and set `GROQ_API_KEY` (get a free key at [console.groq.com/keys](https://console.groq.com/keys)).
3. From project root, run: `python backend/verify_llm.py`.
