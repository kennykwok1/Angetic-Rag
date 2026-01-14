import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

# FAISS 配置
EXCEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "Ballista_仕様書リスト.xlsx",
)
INDEX_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "faiss_index"
)

_vectorstore = None
_embedding_model = None


def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    return _embedding_model


def load_excel_to_documents(excel_path):
    df = pd.read_excel(excel_path, engine="openpyxl")
    docs = []
    for _, row in df.iterrows():
        content = f"項目: {row.get('項目', '')}\nカテゴリ: {row.get('カテゴリ', '')}\nステータス: {row.get('ステータス', '')}\n備考: {row.get('備考', '')}\nメモ: {row.get('メモ', '')}"
        metadata = {
            "仕様書リンク": row.get("仕様書リンク", ""),
            "UI仕様リンク": row.get("UI仕様リンク", ""),
            "完成予定日": str(row.get("完成予定日", "")),
        }
        docs.append(Document(page_content=content, metadata=metadata))
    return docs


def get_vectorstore():
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    embedding = get_embedding_model()
    if os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        _vectorstore = FAISS.load_local(
            INDEX_DIR, embedding, allow_dangerous_deserialization=True
        )
    else:
        if not os.path.exists(EXCEL_PATH):
            print(f"Warning: Excel file not found at {EXCEL_PATH}")
            return None
        os.makedirs(INDEX_DIR, exist_ok=True)
        docs = load_excel_to_documents(EXCEL_PATH)
        _vectorstore = FAISS.from_documents(docs, embedding)
        _vectorstore.save_local(INDEX_DIR)
    return _vectorstore


def local_search(query: str) -> str:
    """从 Excel 向量库检索相关内容"""
    vs = get_vectorstore()
    if vs is None:
        return "Local search unavailable: Vectorstore not initialized."

    docs = vs.similarity_search(query, k=3)
    results = []
    for doc in docs:
        res = (
            f"内容: {doc.page_content}\n链接: {doc.metadata.get('仕様書リンク', 'N/A')}"
        )
        results.append(res)

    return "\n---\n".join(results)


def web_search(query: str, mock: bool = False) -> str:
    """互联网搜索"""
    if mock or not os.getenv("TAVILY_API_KEY"):
        return f"[Web Search] Mock results for: {query}"

    search = TavilySearchResults(max_results=3)
    results = search.invoke(query)

    formatted_res = "\n".join(
        [f"- {r['content']} (Source: {r['url']})" for r in results]
    )
    return formatted_res
