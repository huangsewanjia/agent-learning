TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": (
            "安全读取当前项目目录下的文本文件内容。"
            "支持格式：.txt, .md, .json, .yaml, .yml, .py, .js, .ts, .java, .go, .sql, .csv, .tsv, .log, .xml, .html, .css。"
            "文件大小上限 5MB，超出请使用 offset/tail 参数分段读取。"
            "路径自动锚定到项目根目录，无需关心工具脚本的物理位置。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "相对于项目根目录的【完整文件名（含后缀）】，例如 'docs/intro.md'。如果不确定完整名称，请先调用 search_files 工具搜索"
                },
                "max_lines": {
                    "type": "integer",
                    "description": "最大读取行数，默认 200。大文件建议配合 offset 或 tail 使用"
                },
                "offset": {
                    "type": "integer",
                    "description": "从第几行开始读取（0-indexed），默认 0。用于跳过文件头部"
                },
                "tail": {
                    "type": "boolean",
                    "description": "设为 true 时从文件末尾向前读取 max_lines 行，适用于日志排查场景"
                },
                "encoding": {
                    "type": "string",
                    "description": "文件编码，默认 utf-8。遇到乱码时可尝试 gbk、latin-1 等"
                }
            },
            "required": ["path"]
        }
    }
}