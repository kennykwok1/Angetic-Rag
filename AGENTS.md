# Agentic RAG Repository Guidelines

This document provides essential information for AI agents working on the Agentic RAG project. Follow these conventions to ensure consistency and maintainability.

## 🛠 Build and Development

### Commands
- **Install Dependencies**: `pip install -r requirements.txt`
- **Run Application**: `python main.py` (requires `OPENAI_API_KEY` in `.env`)
- **Run All Tests**: `PYTHONPATH=. pytest`
- **Run Single Test**: `PYTHONPATH=. pytest tests/test_name.py`
- **Linting**: `ruff check .`
- **Formatting**: `ruff format .`

### Environment
- Ensure a `.env` file exists with `OPENAI_API_KEY`.
- LangChain and LangGraph are the core frameworks used for agent orchestration.

## 📏 Code Style Guidelines

### 1. Project Structure
- `app/`: Core logic and application code.
  - `core/`: LangGraph definitions, nodes, and graph structure.
  - `tools/`: External tool integrations (search, etc.).
  - `state.py`: Global `AgentState` definition.
- `tests/`: Pytest test suite mirroring the `app/` structure.
- `docs/`: Documentation and research plans.

### 2. Imports and Naming
- **Absolute Imports**: Always use absolute imports starting from `app.` (e.g., `from app.state import AgentState`).
- **Naming**:
  - Functions and variables: `snake_case`.
  - Classes and TypedDicts: `PascalCase`.
  - Nodes in LangGraph: `snake_case` with `_node` suffix (e.g., `planner_node`).

### 3. Typing
- **Mandatory Types**: Use Python type hints for all function signatures and complex variables.
- **AgentState**: All graph nodes must accept and/or return partial updates to `AgentState` (defined in `app/state.py`).

### 4. Error Handling
- Use `try...except` blocks around LLM invocations and JSON parsing, especially when dealing with unstructured model output.
- Provide sensible fallbacks if an LLM call fails (e.g., returning the original task as a single-step plan).

### 5. LangGraph Patterns
- **Nodes**: Nodes should be stateless functions that take the current `AgentState` and return a dictionary of updates.
- **Conditional Edges**: Logic for routing should be placed in designated functions (e.g., `reviewer_node` returning "continue" or "final").
- **Prompts**: Keep prompts structured. Use f-strings for dynamic content injection.

### 6. Search Tools
- `app/tools/search.py` contains `local_search` and `web_search`.
- Use `mock=True` for web searches during development/testing if an API key for Tavily is not available.

## 🧪 Testing Guidelines
- Use `pytest` for all tests.
- Mock external dependencies (LLMs, Search APIs) where possible to ensure fast and deterministic tests.
- Set `PYTHONPATH=.` when running tests from the root directory.

## 📝 Documentation
- Keep research plans in `docs/plans/` using ISO 8601 date prefixes (e.g., `YYYY-MM-DD-description.md`).
- Update this `AGENTS.md` if significant architectural changes occur.
