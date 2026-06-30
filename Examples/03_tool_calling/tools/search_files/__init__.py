# tools/search_files/__init__.py

# 导出本包的核心接口：工具定义 + 实现函数
from .definitions import TOOL_DEFINITION
from .implementations import search_files

# 可选：显式声明可导出的名称（增强可读性）
__all__ = ["TOOL_DEFINITION", "search_files"]