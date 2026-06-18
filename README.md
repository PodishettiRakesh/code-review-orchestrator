# AI Multi-Agent Code Review Orchestrator

A sophisticated multi-agent AI system for structured code reviews using LangGraph orchestration. This project demonstrates advanced AI automation by simulating specialized code reviewers (Code Quality, Security, Performance) in a coordinated workflow.

## 🎯 Project Overview

This system implements a multi-agent orchestration pattern where each AI agent focuses on a specific aspect of code review:

- **Code Analyzer Agent**: Analyzes code structure, readability, and maintainability
- **Security Agent**: Identifies security vulnerabilities and risks
- **Performance Agent**: Detects performance bottlenecks and inefficiencies
- **Aggregator Agent**: Combines all findings into a structured, actionable report

## 🏗️ Architecture

```
Input → Code Analyzer → Security Agent → Performance Agent → Aggregator Agent → Structured Review Output
```

**Why Multi-Agent?**
- Separation of concerns for focused analysis
- Reduced AI hallucination through scoped prompts
- Extensible architecture for future agents
- Deterministic state management with LangGraph

## 🚀 Current Implementation Status

### ✅ Completed Stages
- **Stage 1**: Environment Setup with Groq LLM integration
- **Stage 2**: State Schema definition with `ReviewState` class

### 🚧 In Progress
- **Stage 3-6**: Agent implementation (Code Analyzer, Security, Performance, Aggregator)
- **Stage 7**: LangGraph workflow orchestration
- **Stage 8**: FastAPI wrapper
- **Stage 9**: React frontend dashboard

## 🛠️ Technology Stack

### Backend
- **Python 3.10+**
- **LangGraph** - Multi-agent orchestration
- **LangChain** - LLM integration framework
- **Groq** - High-performance LLM API (free tier)
- **FastAPI** - REST API framework
- **Uvicorn** - ASGI server

### LLM Provider
- **Groq** - Uses Llama models for fast, cost-effective inference
- Free tier with generous rate limits
- Alternative: Google Gemini (configured in dependencies)

## 📋 Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd code-review-orchestrator
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Groq API key
   # Get a free key at: https://console.groq.com/keys
   ```

5. **Verify LLM connection**
   ```bash
   python backend/verify_llm.py
   ```

## 📁 Project Structure

```
code-review-orchestrator/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App package initialization
│   │   └── state.py             # ReviewState schema (Stage 2)
│   ├── requirements.txt         # Python dependencies
│   └── verify_llm.py           # LLM connection test (Stage 1)
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── ProblemSTatement.txt         # Detailed project specification
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
GROQ_MODEL=llama-3.1-8b-instant
```

### Supported LLM Models
- `llama-3.1-8b-instant` (default, fast)
- `llama-3.1-70b-versatile` (more capable)
- `mixtral-8x7b-32768` (multilingual)

## 📖 Usage (Current State)

Currently, you can verify the LLM connection:

```bash
python backend/verify_llm.py
```

This will test your Groq API connection and confirm Stage 1 completion.

## 🚧 Development Roadmap

### Next Steps
1. **Implement Code Analyzer Agent** - Focus on code structure and quality
2. **Implement Security Agent** - Identify vulnerabilities and security risks
3. **Implement Performance Agent** - Detect performance issues
4. **Create Aggregator Agent** - Combine findings into structured reports
5. **Build LangGraph Workflow** - Orchestrate agent interactions
6. **Develop FastAPI Endpoint** - Create `/analyze` endpoint
7. **Build React Dashboard** - User interface for code submission and review display

### Future Extensions
- Parallel agent execution
- GitHub API integration
- Memory persistence with Redis
- Local Ollama support
- Additional specialized agents (Documentation, Testing, etc.)

## 🤝 Contributing

This project follows the staged implementation approach outlined in `ProblemSTatement.txt`. Each stage builds upon the previous one to demonstrate progressive development of a multi-agent AI system.

## 📚 Why This Approach

**Interview Talking Points:**
- **Multi-agent over single prompt**: Specialized focus reduces hallucination and improves accuracy
- **LangGraph over sequential calls**: Deterministic state management, branching support, and maintainable orchestration
- **State-driven architecture**: Enables complex workflows and future extensibility
- **Separation of concerns**: Each agent has a single responsibility, making the system testable and maintainable

## 📄 License

This project is part of a portfolio demonstration for AI automation engineering capabilities.

---

**Status**: Stages 1-2 Complete | Ready for Agent Implementation
