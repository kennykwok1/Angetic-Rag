import pytest
from app.tools.search import local_search, web_search

def test_local_search_return_type():
    res = local_search("test query")
    assert isinstance(res, str)

def test_web_search_mock():
    # 模拟网页搜索返回
    res = web_search("test query", mock=True)
    assert "Mock results" in res
