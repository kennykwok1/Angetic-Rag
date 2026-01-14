from langgraph.graph import StateGraph, START, END
from app.state import AgentState
from app.core.nodes import (
    clarifier_node,
    planner_node,
    executor_node,
    reviewer_node,
    summarizer_node,
)


def create_research_graph():
    # 1. 初始化图
    workflow = StateGraph(AgentState)

    # 2. 添加节点
    workflow.add_node("clarifier", clarifier_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("summarizer", summarizer_node)

    # 3. 设置边
    workflow.add_edge(START, "clarifier")

    workflow.add_conditional_edges(
        "clarifier",
        lambda state: "proceed" if state.get("is_clarified", True) else "ask",
        {"proceed": "planner", "ask": END},
    )

    workflow.add_edge("planner", "executor")

    # 4. 设置条件边 (Reviewer 逻辑在 edge 中体现)
    workflow.add_conditional_edges(
        "executor", reviewer_node, {"continue": "planner", "final": "summarizer"}
    )

    workflow.add_edge("summarizer", END)

    # 5. 编译
    return workflow.compile()
