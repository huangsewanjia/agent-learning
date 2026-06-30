import requests
import json
from urllib.parse import quote_plus

# 🔒 模拟搜索：实际项目中替换为真实 API（如 Serper.dev）
def web_search(query: str) -> str:
    """模拟搜索结果（演示用），生产环境请替换为真实服务"""
    try:
        # 1. 基础校验
        if not query.strip():
            return "❌ 查询词不能为空"
        if len(query) > 200:
            return "❌ 查询词过长（>200字符）"
        
        # 2. 模拟返回（真实场景：调用 requests.get(...)）
        mock_results = [
            {"title": f"搜索结果 1 for '{query}'", "snippet": "这是模拟的摘要内容，用于演示 Agent 工具调用流程。"},
            {"title": f"搜索结果 2 for '{query}'", "snippet": "Agent 可以将此结果整合进最终回答中。"}
        ]
        
        # 3. 格式化为简洁字符串（避免 LLM 上下文爆炸）
        result_str = "\n".join(
            f"• [{item['title']}]\n  {item['snippet']}" 
            for item in mock_results
        )
        return f"🔍 搜索到 {len(mock_results)} 条结果：\n{result_str}"
    
    except Exception as e:
        return f"❌ 搜索失败：{str(e)}"