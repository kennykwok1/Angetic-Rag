from app.core.graph import create_research_graph
import os
from dotenv import load_dotenv

load_dotenv()

def test_flow():
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping end-to-end test: No API Key")
        return

    app = create_research_graph()
    
    # 模拟一个复杂问题，观察是否触发循环
    query = "对比 2024 年和 2025 年 RAG 技术的主要架构变化"
    
    initial_state = {
        "task": query,
        "plan": [],
        "context": "",
        "steps": [],
        "iteration_count": 0,
        "is_clarified": True
    }

    print(f"Testing with query: {query}")
    # 设置递归上限，防止产生不必要的费用
    result = app.invoke(initial_state)
    
    print("\n[SUCCESS] Final context length:", len(result["context"]))
    assert len(result["context"]) > 100

if __name__ == "__main__":
    test_flow()
