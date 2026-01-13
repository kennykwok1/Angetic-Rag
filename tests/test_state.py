from app.state import AgentState

def test_agent_state_keys():
    # 验证 AgentState 是否包含所有必需的键
    state = AgentState(
        task="test query",
        plan=[],
        context="",
        steps=[],
        iteration_count=0
    )
    assert "task" in state
    assert "iteration_count" in state
    assert state["iteration_count"] == 0
