import json
import os
from langchain_openai import ChatOpenAI
from app.state import AgentState
from app.tools.search import local_search, web_search

# 使用 DeepSeek 模型
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)


def clarifier_node(state: AgentState):
    step = state.get("clarification_step", 0)
    # 如果外部已经标记为已澄清（例如用户选择了跳过引导），则直接通过
    if state.get("is_clarified", False):
        return {"is_clarified": True, "clarification_step": step}

    print(
        f"\n>>> [Clarifier Expert] Analyzing query (Step {step + 1}/3): {state['task'][:50]}..."
    )

    # 如果已经达到 3 步，则强制标记为已澄清，不再询问
    if step >= 3:
        print(">>> [Clarifier Expert] Max steps reached. Proceeding to research.")
        return {"is_clarified": True, "clarification_step": step}

    prompt = f"""
    你是一名资深游戏策划与式样书专家。你的任务是评估用户的问题是否足够具体，以便后续能精准检索式样书。
    
    当前用户问题: {state["task"]}
    当前引导步数: {step}/3
    
    逻辑要求:
    1. **评估具体性**：判断当前问题是否已经足够具体（必须包含或隐含：明确的功能模块、具体子系统、所需信息类型）。
    2. **决策**：
       - 如果问题已经足够具体，或者你认为已经不需要进一步引导，请设置 "is_clarified": true。
       - 如果问题仍然模糊或过于宽泛，且当前步数未达到3步，请设置 "is_clarified": false，并提出一个专业的引导问题。
    3. **引导建议**：
       - 如果需要引导，请提供 3-4 个具体的预设选项供用户选择。
       - 选项中必须包含一个编号为 0 的选项：“直接开始检索 (跳过后续引导)”。
    
    返回 JSON 格式:
    {{
      "is_clarified": boolean,
      "message": "引导性提问内容 (如果 is_clarified 为 false)",
      "options": ["0: 直接开始检索", "1: 选项A", "2: 选项B", ...],
      "reasoning": "为什么判定为已具体或需要进一步引导的详细理由"
    }}
    
    请仅返回 JSON 格式。
    """

    try:
        response = llm.invoke(prompt)
        content = str(response.content).strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        result = json.loads(content)

        # 如果 LLM 认为已明确，则标记为 True
        if result.get("is_clarified", False):
            print(
                f">>> [Clarifier Expert] Query is specific enough. Reasoning: {result.get('reasoning')}"
            )
            return {"is_clarified": True, "clarification_step": step}

        print(
            f">>> [Clarifier Expert] More info needed. Reasoning: {result.get('reasoning')}"
        )
        return {
            "is_clarified": False,
            "clarification_message": result.get("message", "请提供更多细节。"),
            "clarification_options": result.get("options", ["0: 直接开始检索"]),
            "clarification_step": step + 1,
        }
    except Exception as e:
        print(f">>> [Clarifier] Error parsing LLM response: {e}. Proceeding.")
        return {"is_clarified": True}


def planner_node(state: AgentState):
    print(f"\n>>> [Planner] Analyzing task: {state['task'][:50]}...")

    prompt = f"""
    你是一个仕様書检索助手。基于用户问题: {state["task"]}
    以及当前已知上下文: {state["context"]}
    
    请生成 1-3 个具体的检索关键词或子问题，以便从仕様書库中获取更准确的信息。
    仅返回 JSON 字符串列表。
    """

    response = llm.invoke(prompt)
    try:
        content = str(response.content).strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        plan = json.loads(content)
    except:
        plan = [state["task"]]

    print(f">>> [Planner] Generated {len(plan)} research steps.")
    return {"plan": plan}


def executor_node(state: AgentState):
    print(f">>> [Executor] Running research for {len(state['plan'])} queries...")
    new_context = state["context"]

    for query in state["plan"]:
        local_res = local_search(query)
        web_res = web_search(query)
        new_context += f"\n\n### Query: {query}\n{local_res}\n{web_res}"

    return {"context": new_context, "iteration_count": state["iteration_count"] + 1}


def reviewer_node(state: AgentState):
    print(
        f">>> [Reviewer] Evaluating information sufficiency (Iteration {state['iteration_count']})..."
    )

    if state["iteration_count"] >= 5:
        print(">>> [Reviewer] Max iterations reached. Moving to summary.")
        return "final"

    prompt = f"""
    Task: {state["task"]}
    Context: {state["context"]}
    
    Is the information sufficient to provide a final comprehensive report?
    Answer only with 'YES' or 'NO'.
    """

    response = llm.invoke(prompt)
    decision = str(response.content).strip().upper()

    if "YES" in decision:
        print(">>> [Reviewer] Information is sufficient.")
        return "final"
    else:
        print(">>> [Reviewer] More information needed.")
        return "continue"


def summarizer_node(state: AgentState):
    print(">>> [Summarizer] Generating final report...")

    prompt = f"""
    你是一个仕様書检索助手。请根据以下检索到的知识内容，回答用户的问题。
    检索内容包含仕様書链接和UI仕様链接，请在回答中包含这些链接。
    若无相关内容请如实说明。

    用户问题: {state["task"]}
    
    知识内容:
    {state["context"]}
    """

    response = llm.invoke(prompt)
    return {"context": response.content}
