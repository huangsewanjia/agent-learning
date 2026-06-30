TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "通过搜索引擎获取最新信息（模拟，实际需接入 API 如 Serper）",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，例如 '2024年诺贝尔物理学奖得主'"
                }
            },
            "required": ["query"]
        }
    }
}