# 仅定义计算器的 JSON Schema
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "执行安全的数学表达式计算，支持 + - * / () 和小数",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "要计算的数学表达式，例如 '2 + 3 * 4'"
                }
            },
            "required": ["expression"]
        }
    }
}