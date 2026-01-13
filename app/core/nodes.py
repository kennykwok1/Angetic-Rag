import json
import os
from langchain_openai import ChatOpenAI
from app.state import AgentState
from app.tools.search import local_search, web_search

# 使用 DeepSeek 模型
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

def planner_node(state: AgentState):
    print(f"\n>>> [Planner] Analyzing task: {state['task'][:50]}...")
    
    prompt = f"""
    你是一个仕様書检索助手。基于用户问题: {state['task']}
    以及当前已知上下文: {state['context']}
    
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
        plan = [state['task']]
        
    print(f">>> [Planner] Generated {len(plan)} research steps.")
    return {"plan": plan}

def executor_node(state: AgentState):
    print(f">>> [Executor] Running research for {len(state['plan'])} queries...")
    new_context = state['context']
    
    for query in state['plan']:
        local_res = local_search(query)
        web_res = web_search(query, mock=True)
        new_context += f"\n\n### Query: {query}\n{local_res}\n{web_res}"
    
    return {"context": new_context, "iteration_count": state['iteration_count'] + 1}

def reviewer_node(state: AgentState):
    print(f">>> [Reviewer] Evaluating information sufficiency (Iteration {state['iteration_count']})...")
    
    if state['iteration_count'] >= 5:
        print(">>> [Reviewer] Max iterations reached. Moving to summary.")
        return "final"

    prompt = f"""
    Task: {state['task']}
    Context: {state['context']}
    
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

    用户问题: {state['task']}
    
    知识内容:
    {state['context']}
    """
    
    response = llm.invoke(prompt)
    return {"context": response.content}
