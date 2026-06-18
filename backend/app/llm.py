"""
Shared LLM (Groq) for code review agents.
Loads .env from project root and backend/; exposes get_llm() for use by agents.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load .env from project root (parent of backend/) or from backend/
_backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(_backend_dir.parent / ".env")
load_dotenv(_backend_dir / ".env")


def get_llm() -> ChatGroq:
    """Return a configured ChatGroq instance. Requires GROQ_API_KEY in env."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Copy .env.example to .env and add your key. "
            "Get a free key at https://console.groq.com/keys"
        )
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    return ChatGroq(
        model=model,
        groq_api_key=api_key,
        temperature=0,
    )
