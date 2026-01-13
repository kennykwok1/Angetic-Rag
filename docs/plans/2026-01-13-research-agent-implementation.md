# Research Agent Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task in this session.

**Goal:** Build a LangGraph-based Research Agent that cycles through planning, execution (Local/Web search), and reflection.

**Architecture:** A state-graph-based system with nodes for Planning, Execution, Reviewing, and Summarizing. It uses a parallel execution node for search and a conditional edge for looping based on info sufficiency.

**Tech Stack:** LangGraph, LangChain, OpenAI, Tavily, ChromaDB, Python 3.14.

---

### Task 1: Define State and Schema

**Files:**
- Create: `app/state.py`
- Test: `tests/test_state.py`

**Step 1: Write the failing test**
Create `tests/test_state.py` to verify the `AgentState` TypedDict structure.

**Step 2: Run test to verify it fails**
Run: `.venv/bin/pytest tests/test_state.py`

**Step 3: Write minimal implementation**
Define `AgentState` in `app/state.py` with `task`, `plan`, `context`, `steps`, and `iteration_count`.

**Step 4: Run test to verify it passes**
Run: `.venv/bin/pytest tests/test_state.py`

**Step 5: Commit**
`git add app/state.py tests/test_state.py && git commit -m "feat: define agent state schema"`

---

### Task 2: Implement Search Tools

**Files:**
- Create: `app/tools/search.py`
- Test: `tests/test_tools.py`

**Step 1: Write failing tests for tools**
Verify `local_search` and `web_search` return expected structures.

**Step 2: Implement search tools**
- `local_search`: Mock ChromaDB for now.
- `web_search`: Use `TavilySearchResults`.

**Step 3: Run tests and Commit**

---

### Task 3: Implement Graph Nodes

**Files:**
- Create: `app/core/nodes.py`
- Test: `tests/test_nodes.py`

**Step 1: Implement Planner node**
Prompt LLM to generate a JSON plan based on task and context.

**Step 2: Implement Executor node**
Call search tools and update context.

**Step 3: Implement Reviewer node**
Check sufficiency and update loop counter.

**Step 4: Implement Summarizer node**
Generate final response.

---

### Task 4: Assemble and Compile Graph

**Files:**
- Create: `app/core/graph.py`
- Create: `main.py`

**Step 1: Construct StateGraph**
Connect nodes: `START -> Planner -> Executor -> Reviewer`.
Add conditional edge: `Reviewer -> Planner` or `Reviewer -> Summarizer`.

**Step 2: Implement logging and entry point**
In `main.py`, use `graph.stream` to print intermediate steps with colors/labels.

**Step 3: End-to-end Test**
Run a sample query.

