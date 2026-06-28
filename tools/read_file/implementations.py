import os
from pathlib import Path

# ==================== 🔧 核心修改区：标记文件锚定法 ====================
def find_project_root(start_path: Path, marker: str = ".gitignore") -> Path:
    """
    从 start_path 开始向上逐级查找包含 marker 文件的目录。
    找到即返回该目录作为 PROJECT_ROOT；找不到则抛出明确异常。
    """
    current = start_path.resolve()
    for _ in range(10):  # 最多向上查找 10 级，防止无限循环
        if (current / marker).exists():
            return current
        parent = current.parent
        if parent == current:  # 已到达磁盘根目录，无法再向上
            break
        current = parent
    raise FileNotFoundError(
        f"❌ 未找到项目根目录标记文件 '{marker}'。\n"
        f"请在项目根目录下创建该文件，或检查 marker 名称是否正确。\n"
        f"当前搜索起点: {start_path.resolve()}"
    )

# 👇 用标记文件锚定，彻底摆脱对 read_file.py 物理位置的依赖
PROJECT_ROOT = find_project_root(Path(__file__))
# ======================================================================

# 扩展白名单：覆盖代码、数据、配置文件
ALLOWED_EXTS = {
    '.txt', '.md', '.json', '.yaml', '.yml',
    '.py', '.js', '.ts', '.java', '.go', '.sql',
    '.csv', '.tsv', '.log', '.xml', '.html', '.css'
}


def read_file(
    path: str,
    max_lines: int = 200,
    offset: int = 0,
    tail: bool = False,
    encoding: str = "utf-8"
) -> str:
    """企业级安全文件读取工具"""
    try:
        full_path = (PROJECT_ROOT / path).resolve()

        # 🔒 安全检查
        if not full_path.is_relative_to(PROJECT_ROOT):
            return "❌ 安全拒绝：路径超出允许范围"
        if full_path.suffix.lower() not in ALLOWED_EXTS:
            return f"❌ 不支持的文件类型 '{full_path.suffix}'"
        if not full_path.exists():
            return f"❌ 文件不存在：{path}"
        if full_path.stat().st_size > 5 * 1024 * 1024:
            return "❌ 文件过大（>5MB），请使用 offset/tail 分段读取"

        # 📖 智能读取逻辑
        with open(full_path, 'r', encoding=encoding, errors='replace') as f:
            all_lines = f.readlines()

        total_lines = len(all_lines)

        if tail:
            selected = all_lines[-max_lines:] if total_lines > max_lines else all_lines
            hint = f"(最后 {len(selected)} 行)"
        else:
            end = min(offset + max_lines, total_lines)
            selected = all_lines[offset:end]
            hint = f"(第 {offset + 1}-{end} 行)" if selected else "(无内容)"

        content = "".join(selected)
        return f"✅ 读取成功 {hint}，共 {total_lines} 行:\n{content}"

    except UnicodeDecodeError:
        return f"❌ 编码错误，请尝试指定 encoding 参数（当前: {encoding}）"
    except FileNotFoundError as e:
        # 捕获标记文件未找到的异常，给出清晰提示
        return str(e)
    except Exception as e:
        return f"❌ 读取失败：{str(e)}"