# tools/__init__.py
from .calculator import TOOL_DEFINITION as calc_def, calculator as calc_impl
from .read_file import TOOL_DEFINITION as file_def, read_file as file_impl
from .search import TOOL_DEFINITION as search_def, web_search as search_impl
from .search_files import TOOL_DEFINITION as search_files_def, search_files as search_files_impl

# ✅ 对外暴露的两个核心对象
TOOLS = [
    calc_def,
    file_def,
    search_def,
    search_files_def,
]

TOOL_FUNCTIONS = {
    calc_def["function"]["name"]: calc_impl,
    file_def["function"]["name"]: file_impl,
    search_def["function"]["name"]: search_impl,
    search_files_def["function"]["name"]: search_files_impl,
}

__all__ = ["TOOLS", "TOOL_FUNCTIONS"]