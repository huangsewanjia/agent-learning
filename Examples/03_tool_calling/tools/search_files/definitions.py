# tools/search_files/definitions.py

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "search_files",
        "description": "在当前项目根目录下模糊搜索文件名（大小写不敏感）。当用户不确定文件路径时，应先调用此工具定位文件，再用 read_file 读取。",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "文件名关键词（如 'config', 'log', '*.py'），支持部分匹配"
                },
                "max_results": {
                    "type": "integer",
                    "description": "最多返回结果数，默认为 10",
                    "default": 10
                }
            },
            "required": ["keyword"]
        }
    }
}