# Research Agent Design: LangGraph-based Agentic RAG

## Overview
A deep-research agent that autonomously cycles through planning, execution (local & web search), and reflection to answer complex queries.

## Architecture: Plan-Execute-Review (Option B)
The system is implemented as a StateGraph in LangGraph.

### State Definition
- `task`: Original user query.
- `plan`: Current list of research questions.
- `context`: Aggregated information from all sources.
- `steps`: Execution history for logging.
- `iteration_count`: Counter to prevent infinite loops (max 5).

### Nodes
1. **Planner**: Analyzes context and task to generate/update the search plan.
2. **Executor**: Concurrent execution of:
   - `Local_Search`: Vector DB retrieval (ChromaDB).
   - `Web_Search`: Internet retrieval (Tavily).
3. **Reviewer**: Evaluates if context is sufficient.
   - If sufficient -> **Summarizer**.
   - If insufficient -> **Planner**.
4. **Summarizer**: Final report generation.

## Logging
- Each node outputs its reasoning and decisions to the console for transparency.
- Format: `>>> [NodeName] Decision/Action details`.

## Tools
- **LLM**: OpenAI (GPT-4o or similar).
- **Search**: Tavily API.
- **Vector DB**: ChromaDB.
