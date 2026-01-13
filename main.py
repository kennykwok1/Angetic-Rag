import os
import io
from PIL import Image as PILImage
from dotenv import load_dotenv
from app.core.graph import create_research_graph
from app.state import AgentState

load_dotenv()

def main():
    # 检查环境变量
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Error: DEEPSEEK_API_KEY not found in environment.")
        return

    # 创建图
    app = create_research_graph()

    # 显示 Graph (仿照 test4.py)
    try:
        print(">>> 正在生成流程图...")
        img_bytes = app.get_graph().draw_mermaid_png()
        PILImage.open(io.BytesIO(img_bytes)).show()
    except Exception as e:
        print(f">>> 无法显示流程图: {e} (这通常是因为缺少绘图依赖或运行在无界面环境)")

    print("\n=== Agentic RAG 研究助手 (DeepSeek + Excel) ===")
    print("(输入 'exit', 'quit' 或 'q' 退出)\n")

    while True:
        query = input("请输入您的研究课题: ").strip()
        if not query:
            continue
        if query.lower() in {"exit", "quit", "q"}:
            break
        
        initial_state: AgentState = {
            "task": query,
            "plan": [],
            "context": "",
            "steps": [],
            "iteration_count": 0
        }

        # 执行并流式输出状态变化（可选）
        print(f"\n--- 开始研究: {query} ---")
        try:
            # 这里可以使用 stream 来展示进度
            final_state = app.invoke(initial_state)
            
            print("\n--- 最终研究报告 ---")
            print(final_state["context"])
            print("\n" + "="*40 + "\n")
        except Exception as e:
            print(f"\n[Error] 发生错误: {e}\n")

if __name__ == "__main__":
    main()
