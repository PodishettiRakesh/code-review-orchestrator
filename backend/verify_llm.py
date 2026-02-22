"""
Stage 1: Verify a single LLM call (Groq).
Run from project root: python backend/verify_llm.py
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load .env from project root (parent of backend/) or from backend/
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")


def main() -> None:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(
            "ERROR: GROQ_API_KEY not set. Copy .env.example to .env and add your key.\n"
            "Get a free key at https://console.groq.com/keys"
        )
        raise SystemExit(1)

    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    llm = ChatGroq(
        model=model,
        groq_api_key=api_key,
        temperature=0,
    )

    response = llm.invoke("Reply with one short sentence.")
    print(response.content)
    print("\nStage 1 OK: Single LLM call succeeded (Groq).")


if __name__ == "__main__":
    main()
