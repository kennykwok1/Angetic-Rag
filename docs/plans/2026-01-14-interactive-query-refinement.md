# Interactive Query Refinement Plan

## Overview
Add an interactive clarification step to the RAG pipeline to ensure user queries are sufficiently detailed and clear before initiating the expensive research and retrieval process.

## Goals
- Identify vague or underspecified user queries.
- Proactively ask the user for missing information.
- Refine the `task` in `AgentState` based on user feedback.

## Proposed Changes

### 1. State Definition (`app/state.py`)
Update `AgentState` to include:
- `is_clarified`: A boolean flag indicating if the query is ready for research.
- `clarification_message`: The question to be presented to the user if more info is needed.

### 2. New Node: `clarifier_node` (`app/core/nodes.py`)
- **Logic**: 
    - Use an LLM to evaluate the current `task`.
    - If the query is clear and specific, set `is_clarified = True`.
    - If the query is vague, set `is_clarified = False` and generate a `clarification_message` asking for specific missing details.
- **Prompt**:
    ```text
    Evaluate if the following user query is clear and specific enough to retrieve information from technical specifications:
    "{task}"
    
    If it's clear, return JSON: {"is_clarified": true, "message": ""}
    If it's vague, return JSON: {"is_clarified": false, "message": "Your clarifying question here"}
    ```

### 3. Graph Workflow (`app/core/graph.py`)
- **Node Insertion**: Add `clarifier` as the first node after `START`.
- **Conditional Routing**:
    - `START` -> `clarifier`
    - `clarifier` --(is_clarified?)--> 
        - `True` -> `planner`
        - `False` -> `END` (Wait for user input)

## Execution Steps
1. Modify `app/state.py` to update `AgentState`.
2. Add `clarifier_node` implementation in `app/core/nodes.py`.
3. Update `app/core/graph.py` to integrate the new node and routing logic.
