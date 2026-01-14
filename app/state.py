from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    task: str
    plan: List[str]
    context: str
    steps: List[Dict[str, Any]]
    iteration_count: int
    is_clarified: bool
    clarification_message: str
    clarification_step: int
    clarification_options: List[str]
