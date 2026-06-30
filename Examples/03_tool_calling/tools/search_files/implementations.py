# tools/search_files/implementations.py
from pathlib import Path

# ==============================
# 1. 自动定位项目根目录（基于 .gitignore）
# ==============================
def _find_project_root(start_path: Path, marker: str = ".gitignore") -> Path:
    current = start_path.resolve()
    for _ in range(10):
        if (current / marker).exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    raise RuntimeError(
        f"❌ 未找到项目根目录标记文件 '{marker}'。\n"
        f"请确认 {marker} 存在于项目根目录（与 tools/ 同级）"
    )

_PROJECT_ROOT = _find_project_root(Path(__file__))

# ==============================
# 2. 工具实现函数
# ==============================
def search_files(keyword: str, max_results: int = 10) -> str:
    """模糊搜索项目中的文件"""
    try:
        matches = []
        for p in _PROJECT_ROOT.rglob("*"):
            if p.is_file() and keyword.lower() in p.name.lower():
                rel_path = p.relative_to(_PROJECT_ROOT)
                matches.append(str(rel_path))
                if len(matches) >= max_results:
                    break

        if not matches:
            return f"🔍 未找到包含 '{keyword}' 的文件。请尝试更宽泛的关键词（如 'config', 'test', '*.py'）。"

        result_lines = [f"  - {m}" for m in matches]
        return (
            f"🔍 找到 {len(matches)} 个匹配文件（相对于项目根目录）：\n" +
            "\n".join(result_lines) +
            "\n\n💡 建议：将上述完整路径传给 read_file 工具读取内容。"
        )
    except Exception as e:
        return f"❌ 搜索失败：{type(e).__name__}: {str(e)}"