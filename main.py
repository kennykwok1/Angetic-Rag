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
            "iteration_count": 0,
            "is_clarified": False,
            "clarification_message": "",
            "clarification_step": 0,
            "clarification_options": []
        }

        # 执行并流式输出状态变化（可选）
        print(f"\n--- 开始研究: {query} ---")
        try:
            current_state = initial_state
            while True:
                final_state = app.invoke(current_state)
                
                if final_state.get("is_clarified", True):
                    print("\n--- 最终研究报告 ---")
                    print(final_state["context"])
                    print("\n" + "="*40 + "\n")
                    break
                else:
                    print(f"\n[专家建议] {final_state['clarification_message']}")
                    options = final_state.get("clarification_options", [])
                    for opt in options:
                        print(f"  {opt}")
                    
                    user_input = input("\n请选择编号或补充信息 (输入 'c' 取消, '0' 直接开始): ").strip()
                    
                    if user_input.lower() == 'c':
                        print("已取消当前研究课题。")
                        break
                    
                    # 处理选项选择
                    selected_text = user_input
                    if user_input.isdigit():
                        idx = int(user_input)
                        # 如果选择 0，标记为已澄清并继续
                        if idx == 0:
                            current_state = final_state
                            current_state["is_clarified"] = True
                            print("\n>>> 用户选择直接开始检索...")
                            continue
                            
                        # 查找匹配的选项文本
                        for opt in options:
                            if opt.startswith(f"{idx}:"):
                                selected_text = opt.split(":", 1)[1].strip()
                                break
                    
                    # 更新 task 并重新开始
                    current_state = final_state
                    current_state["task"] = f"{current_state['task']} (补充: {selected_text})"
                    # 重置 clarification 状态以便重新检查
                    current_state["is_clarified"] = False 
                    print(f"\n--- 细化课题: {current_state['task']} ---")

        except Exception as e:
            print(f"\n[Error] 发生错误: {e}\n")

if __name__ == "__main__":
    main()
